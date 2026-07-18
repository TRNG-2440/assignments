from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path
from typing import Any, Dict

os.environ.setdefault(
    "PYSPARK_SUBMIT_ARGS",
    "--conf spark.ui.showConsoleProgress=false pyspark-shell",
)

from pyspark.sql import SparkSession


def prepare_spark_input(source_path: Path) -> str:
    """Copy CSV to a simple Windows-safe Spark input folder."""
    source_path = source_path.resolve()
    if os.name == "nt":
        target_dir = Path("C:/spark_rdd_input")
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / source_path.name
        shutil.copy2(source_path, target_file)
        return target_file.as_posix()
    return source_path.as_posix()


def create_spark() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("HealthcarePatientVisitRDD")
        .master("local[4]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.local.dir", "C:/spark-temp" if os.name == "nt" else "/tmp/spark-temp")
        .config("spark.sql.warehouse.dir", "C:/spark-warehouse" if os.name == "nt" else "/tmp/spark-warehouse")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def parse_line(line: str) -> Dict[str, Any]:
    row = next(csv.reader([line]))
    return {
        "visit_id": row[0].strip(),
        "visit_date": row[1].strip(),
        "patient_id": row[2].strip(),
        "patient_name": row[3].strip(),
        "age": int(row[4]),
        "city": row[5].strip(),
        "department": row[6].strip(),
        "doctor_id": row[7].strip(),
        "visit_type": row[8].strip(),
        "diagnosis": row[9].strip(),
        "bill_amount": float(row[10]),
        "payment_status": row[11].strip().upper(),
        "rating": int(row[12]),
    }


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    csv_path = project_dir / "healthcare_patient_visits.csv"
    spark_csv_path = prepare_spark_input(csv_path)

    spark = create_spark()
    sc = spark.sparkContext

    missing_city_acc = sc.accumulator(0)
    invalid_age_acc = sc.accumulator(0)
    invalid_bill_acc = sc.accumulator(0)
    invalid_status_acc = sc.accumulator(0)
    invalid_total_acc = sc.accumulator(0)

    allowed_statuses = {"PAID", "PENDING", "CANCELLED"}

    service_charge_map = {
        "Cardiology": 0.18,
        "Orthopedics": 0.12,
        "Dermatology": 0.08,
        "Neurology": 0.15,
        "General Medicine": 0.05,
    }
    service_charge_bc = sc.broadcast(service_charge_map)

    def validate(record: Dict[str, Any]) -> bool:
        is_valid = True
        if not record["city"]:
            missing_city_acc.add(1)
            is_valid = False
        if record["age"] <= 0:
            invalid_age_acc.add(1)
            is_valid = False
        if record["bill_amount"] <= 0:
            invalid_bill_acc.add(1)
            is_valid = False
        if record["payment_status"] not in allowed_statuses:
            invalid_status_acc.add(1)
            is_valid = False
        if not is_valid:
            invalid_total_acc.add(1)
        return is_valid

    def enrich(record: Dict[str, Any]) -> Dict[str, Any]:
        pct = service_charge_bc.value.get(record["department"], 0.0)
        service_charge = record["bill_amount"] * pct
        final_amount = record["bill_amount"] + service_charge
        return {
            **record,
            "service_charge_pct": pct,
            "service_charge": round(service_charge, 2),
            "final_amount": round(final_amount, 2),
        }

    try:
        raw_rdd = sc.textFile(spark_csv_path, minPartitions=4)
        header = raw_rdd.first()

        data_rdd = raw_rdd.filter(lambda line: line != header and bool(line.strip()))
        parsed_rdd = data_rdd.map(parse_line).cache()

        valid_rdd = parsed_rdd.filter(validate).cache()
        enriched_rdd = valid_rdd.map(enrich).cache()
        paid_rdd = enriched_rdd.filter(lambda r: r["payment_status"] == "PAID").cache()

        total_rows = data_rdd.count()
        valid_rows = valid_rdd.count()
        invalid_rows = invalid_total_acc.value

        print("=== VALIDATION RESULTS ===")
        print("Total data rows:", total_rows)
        print("Valid rows:", valid_rows)
        print("Invalid total:", invalid_rows)
        print("Missing city:", missing_city_acc.value)
        print("Invalid age:", invalid_age_acc.value)
        print("Invalid bill:", invalid_bill_acc.value)
        print("Invalid status:", invalid_status_acc.value)

        print("\n=== ACTION DEMOS ===")
        print("First valid record:")
        print(enriched_rdd.first())

        print("\nTake 5 valid records:")
        print(enriched_rdd.take(5))

        print("\nVisit count by city using countByValue:")
        print(enriched_rdd.map(lambda r: r["city"]).countByValue())

        total_final_revenue = enriched_rdd.map(lambda r: r["final_amount"]).reduce(lambda a, b: a + b)
        print("\nTotal final revenue using reduce:")
        print(round(total_final_revenue, 2))

        print("\n=== REQUIRED ANALYTICS ===")

        visits_by_city = (
            enriched_rdd
            .map(lambda r: (r["city"], 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda x: x[0])
        )
        print("Visits by city:")
        print(visits_by_city.collect())

        visits_by_department = (
            enriched_rdd
            .map(lambda r: (r["department"], 1))
            .reduceByKey(lambda a, b: a + b)
            .sortBy(lambda x: x[0])
        )
        print("\nVisits by department:")
        print(visits_by_department.collect())

        revenue_by_city = (
            paid_rdd
            .map(lambda r: (r["city"], r["final_amount"]))
            .reduceByKey(lambda a, b: a + b)
            .mapValues(lambda amt: round(amt, 2))
            .sortBy(lambda pair: pair[1], ascending=False)
        )
        print("\nRevenue by city:")
        print(revenue_by_city.collect())

        revenue_by_department = (
            paid_rdd
            .map(lambda r: (r["department"], r["final_amount"]))
            .reduceByKey(lambda a, b: a + b)
            .mapValues(lambda amt: round(amt, 2))
            .sortBy(lambda pair: pair[1], ascending=False)
        )
        print("\nRevenue by department:")
        print(revenue_by_department.collect())

        print("\nTop 3 paid visits:")
        print(
            paid_rdd.takeOrdered(
                3,
                key=lambda r: -r["final_amount"],
            )
        )

        emergency_departments = (
            enriched_rdd
            .filter(lambda r: r["visit_type"] == "Emergency")
            .map(lambda r: r["department"])
            .distinct()
            .sortBy(lambda x: x)
        )
        print("\nDepartments handling emergency visits:")
        print(emergency_departments.collect())

        print("\nDistinct cities:")
        print(enriched_rdd.map(lambda r: r["city"]).distinct().sortBy(lambda x: x).collect())

        print("\nDistinct departments:")
        print(enriched_rdd.map(lambda r: r["department"]).distinct().sortBy(lambda x: x).collect())

        avg_rating_by_department = (
            enriched_rdd
            .map(lambda r: (r["department"], (r["rating"], 1)))
            .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
            .mapValues(lambda x: round(x[0] / x[1], 2))
            .sortBy(lambda x: x[1], ascending=False)
        )
        print("\nAverage rating by department:")
        print(avg_rating_by_department.collect())

        print("\nDepartment with highest average patient rating:")
        print(avg_rating_by_department.take(1))

        print("\n=== EXTRA TRANSFORMATIONS ===")
        print("Tags using flatMap:")
        print(
            enriched_rdd
            .flatMap(lambda r: [f"city:{r['city']}", f"dept:{r['department']}", f"type:{r['visit_type']}"])
            .map(lambda tag: (tag, 1))
            .reduceByKey(lambda a, b: a + b)
            .sortByKey()
            .collect()
        )

        print("\nVisit IDs grouped by department:")
        print(
            enriched_rdd
            .map(lambda r: (r["department"], r["visit_id"]))
            .groupByKey()
            .mapValues(lambda ids: sorted(list(ids)))
            .sortByKey()
            .collect()
        )

        opd_patients = enriched_rdd.filter(lambda r: r["visit_type"] == "OPD").map(lambda r: r["patient_id"])
        emergency_patients = enriched_rdd.filter(lambda r: r["visit_type"] == "Emergency").map(lambda r: r["patient_id"])
        print("\nUnique OPD or Emergency patient IDs using union:")
        print(opd_patients.union(emergency_patients).distinct().sortBy(lambda x: x).collect())

        print("\nPartition demo:")
        repartitioned_rdd = enriched_rdd.repartition(6)
        coalesced_rdd = repartitioned_rdd.coalesce(2)
        print("Original:", enriched_rdd.getNumPartitions())
        print("Repartitioned:", repartitioned_rdd.getNumPartitions())
        print("Coalesced:", coalesced_rdd.getNumPartitions())

        print("\n=== FOREACH DEMO ===")
        visit_id_lengths = sc.accumulator(0)

        def count_visit_id_length(record: Dict[str, Any]) -> None:
            visit_id_lengths.add(len(record["visit_id"]))

        enriched_rdd.foreach(count_visit_id_length)
        print("Total visit_id character count from foreach():", visit_id_lengths.value)

        print("\nBroadcast variable used in enrich() to look up department service charge %.")
        print("Accumulators used in validate() to count invalid records.")

    finally:
        service_charge_bc.unpersist()
        spark.stop()


if __name__ == "__main__":
    main()