from pyspark.sql import SparkSession
from pathlib import Path
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "healthcare_patient_visits.csv"


def main():

    # PART A - Spark + RDD
    spark = (
        SparkSession.builder
        .appName("Healthcare Patient Visit Analytics")
        .master("local[*]")
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    print("Spark Started")
    print("File:", FILE_PATH)

    rdd = sc.textFile(str(FILE_PATH))

    header = rdd.first()

    rdd = rdd.filter(lambda row: row != header)

    print("Total rows:", rdd.count())

    # PART B - Accumulators
    missing_city = sc.accumulator(0)
    invalid_age = sc.accumulator(0)
    invalid_bill = sc.accumulator(0)
    invalid_payment = sc.accumulator(0)
    invalid_records = sc.accumulator(0)


    VALID_STATUS = {
        "PAID",
        "PENDING",
        "CANCELLED"
    }

    def parse_record(line):

        fields = line.split(",")

        record = {
            "visit_id": fields[0],
            "visit_date": fields[1],
            "patient_id": fields[2],
            "patient_name": fields[3],
            "age": int(fields[4]),
            "city": fields[5],
            "department": fields[6],
            "doctor_id": fields[7],
            "visit_type": fields[8],
            "diagnosis": fields[9],
            "bill_amount": float(fields[10]),
            "payment_status": fields[11],
            "rating": int(fields[12])
        }

        if record["city"] == "":
            missing_city.add(1)

        if record["age"] <= 0:
            invalid_age.add(1)

        if record["bill_amount"] <= 0:
            invalid_bill.add(1)

        if record["payment_status"] not in VALID_STATUS:
            invalid_payment.add(1)

        if (
            record["city"] == ""
            or record["age"] <= 0
            or record["bill_amount"] <= 0
            or record["payment_status"] not in VALID_STATUS
        ):
            invalid_records.add(1)

        return record

    records = rdd.map(parse_record)

    valid_records = records.filter(
        lambda x:
            x["city"] != ""
            and x["age"] > 0
            and x["bill_amount"] > 0
            and x["payment_status"] in VALID_STATUS
    )

    # force accumulator execution
    records.count()

    print("\n=== Validation Results ===")
    print("Missing city:", missing_city.value)
    print("Invalid age:", invalid_age.value)
    print("Invalid bill:", invalid_bill.value)
    print("Invalid payment:", invalid_payment.value)
    print("Invalid records:", invalid_records.value)


    # PART C - Broadcast
    service_charge_map = {

        "Cardiology":0.18,
        "Orthopedics":0.12,
        "Dermatology":0.08,
        "Neurology":0.15,
        "General Medicine":0.05

    }

    service_charge_bc = sc.broadcast(service_charge_map)

    def add_charge(record):

        pct = service_charge_bc.value.get(
            record["department"],
            0
        )

        record["service_charge"] = (
            record["bill_amount"] * pct
        )

        record["final_amount"] = (
            record["bill_amount"]
            +
            record["service_charge"]
        )

        return record


    valid_records = valid_records.map(add_charge)

    valid_records.cache()

    # PART D - Transformations

    # filter()
    paid_records = valid_records.filter(
        lambda x:x["payment_status"]=="PAID"
    )


    # flatMap()
    tags = valid_records.flatMap(
        lambda x:[
            f"city:{x['city']}",
            f"dept:{x['department']}",
            f"type:{x['visit_type']}"
        ]
    )

    print("\nTags:")
    print(tags.take(10))

    # distinct()
    cities = (
        valid_records
        .map(lambda x:x["city"])
        .distinct()
        .collect()
    )

    departments = (
        valid_records
        .map(lambda x:x["department"])
        .distinct()
        .collect()
    )

    print("\nCities:", cities)
    print("Departments:", departments)

    # mapValues()
    amount_pairs = (
        valid_records
        .map(lambda x:(x["city"],x["final_amount"]))
        .mapValues(lambda x:round(x,2))
    )

    # reduceByKey()
    revenue_city = (
        valid_records
        .map(lambda x:(x["city"],x["final_amount"]))
        .reduceByKey(lambda a,b:a+b)
        .collect()
    )

    print("\nRevenue by City:")
    for city,amount in revenue_city:
        print(f"{city}: {amount}")

    # groupByKey()
    visits_department = (
        valid_records
        .map(lambda x:(x["department"],x["visit_id"]))
        .groupByKey()
        .mapValues(list)
        .collect()
    )

    print("\nVisits by Department:")
    for department,visits in visits_department:
        print(f"{department}: {len(visits)}")

    # sortBy()
    sorted_departments = (
        valid_records
        .map(lambda x:(x["department"],x["final_amount"]))
        .reduceByKey(lambda a,b:a+b)
        .sortBy(lambda x:x[1],ascending=False)
        .collect()
    )

    print("\nDepartment Revenue:")
    print(sorted_departments)

    # union()
    opd = (
        valid_records
        .filter(lambda x:x["visit_type"]=="OPD")
        .map(lambda x:x["visit_id"])
    )

    emergency = (
        valid_records
        .filter(lambda x:x["visit_type"]=="EMERGENCY")
        .map(lambda x:x["visit_id"])
    )

    print("\nCombined visits:")
    print(opd.union(emergency).collect())

    # repartition/coalesce
    print(
        "\nPartitions:",
        valid_records.getNumPartitions()
    )

    valid_records = valid_records.repartition(4)

    print(
        "After repartition:",
        valid_records.getNumPartitions()
    )

    valid_records = valid_records.coalesce(2)

    print(
        "After coalesce:",
        valid_records.getNumPartitions()
    )

    # PART E - Actions
    print("\nCount:", valid_records.count())

    print("First:")
    print(valid_records.first())

    print("Take (Top 3):")
    print(valid_records.take(3))


    print("\nCount by payment:")
    print(
        valid_records
        .map(lambda x:x["payment_status"])
        .countByValue()
    )

    print("\nTop 3 Paid Visits:")

    top_paid = (
        paid_records
        .map(lambda x:(x["visit_id"],x["final_amount"]))
        .takeOrdered(
            3,
            key=lambda x:-x[1]
        )
    )

    print(top_paid)

    # foreach accumulator example
    validation_counter = sc.accumulator(0)

    def check_rating(x):

        if x["rating"] > 0:
            validation_counter.add(1)


    valid_records.foreach(check_rating)

    print(
        "\nRatings validated:",
        validation_counter.value
    )

    spark.stop()


if __name__ == "__main__":
    main()