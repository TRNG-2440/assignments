from pyspark.sql import SparkSession
from pyspark.sql import functions

# Part A
# create spark session
spark = (
    SparkSession.builder
    .appName("healthcareRDD")
    .master("local[*]")
    .getOrCreate()
)

# rdd using csv file
healthcare = spark.sparkContext.textFile("healthcare_rdd_assignment_pack/healthcare_patient_visits.csv")
# remove header
header = healthcare.first()
healthcare = healthcare.filter(lambda row: row != header)

# parse row into dictionary
def parse_into_dictionary(row):
    row_list = row.split(",")
    header_list = header.split(",")
    return {
        header_list[0]: row_list[0].strip(),
        header_list[1]: row_list[1].strip(),
        header_list[2]: row_list[2].strip(),
        header_list[3]: row_list[3].strip(),
        header_list[4]: int(row_list[4].strip()),
        header_list[5]: row_list[5].strip(),
        header_list[6]: row_list[6].strip(),
        header_list[7]: row_list[7].strip(),
        header_list[8]: row_list[8].strip(),
        header_list[9]: row_list[9].strip(),
        header_list[10]: int(row_list[10].strip()),
        header_list[11]: row_list[11].strip().upper(),
        header_list[12]: int(row_list[12].strip())
    }

parsed_healthcare = healthcare.map(parse_into_dictionary).cache()

# Part B
# create accumulators
missing_cities_acc = spark.sparkContext.accumulator(0)
invalid_ages_acc = spark.sparkContext.accumulator(0) 
invalid_bills_acc = spark.sparkContext.accumulator(0)
invalid_payment_status_acc = spark.sparkContext.accumulator(0)
total_invalid_acc = spark.sparkContext.accumulator(0)

def check_invalid(row):
    valid = True

    if not row["city"]:
        missing_cities_acc.add(1)
        valid = False
    if row["age"] <= 0:
        invalid_ages_acc.add(1)
        valid = False
    if row["bill_amount"] <= 0:
        invalid_bills_acc.add(1)
        valid = False
    if not (row["payment_status"] == "PAID" or row["payment_status"] == "PENDING" or row["payment_status"] == "CANCELLED"):
        invalid_payment_status_acc.add(1)
        valid = False
    if not valid:
        total_invalid_acc.add(1)

    return valid
# clean RDD
cleaned_healthcare = parsed_healthcare.filter(check_invalid).cache()

# Part C
# Create broadcast variable
service_charge_map = {
    "Cardiology": 0.18,
    "Orthopedics": 0.12,
    "Dermatology": 0.08,
    "Neurology": 0.15,
    "General Medicine": 0.05
}

def total_charge(row):
    service_charge = row["bill_amount"] * service_charge_map[row["department"]]
    total_charge = row["bill_amount"] + service_charge

    row["service_charge_percentage"] = service_charge_map[row["department"]]
    row["service_charge"] = round(service_charge, 2)
    row["total_charge"] = round(total_charge, 2)
    return row

# Part D, E, F
# create total_charge column
final_healthcare = cleaned_healthcare.map(total_charge).cache()

# total data rows available
print(f"Total Records: {parsed_healthcare.count()}")
# valid and invalid rows
print(f"Valid Records: {cleaned_healthcare.count()}")
print(f"Invalid Records: {total_invalid_acc}")
print(f"Missing City: {missing_cities_acc}")
print(f"Invalid Age: {invalid_ages_acc}")
print(f"Invalid Bill Amount: {invalid_bills_acc}")
print(f"Invalid Payment Status: {invalid_payment_status_acc}")
print()
# visits per city
visits_per_city = final_healthcare.map(lambda row: row["city"]).countByValue()
print(f"Visits per city: {dict(visits_per_city)}")
print()
# visits per department
visits_per_department = final_healthcare.map(lambda row: row["department"]).countByValue()
print(f"Visits per department: {dict(visits_per_department)}")
print()
# final revenue by city
paid_healthcare = final_healthcare.filter(lambda row: row["payment_status"] == "PAID").cache()
total_revenue_by_city = (paid_healthcare
                         .map(lambda row: (row["city"], row["total_charge"]))
                         .reduceByKey(lambda a, b: a + b)
                         .sortBy(lambda row: row[1], False)
                         )
print(f"Revenue per city: {total_revenue_by_city.collect()}")
print()
# final revenue by department
total_revenue_by_department = (paid_healthcare
                         .map(lambda row: (row["department"], row["total_charge"]))
                         .reduceByKey(lambda a, b: a + b)
                         .sortBy(lambda row: row[1], False)
                         )
print(f"Revenue per department: {total_revenue_by_department.collect()}")
print()
# Top 3 paid visits
top_3_visits = (paid_healthcare.takeOrdered(3, lambda row: row["total_charge"]))
print(f"Top 3 paid visits: {top_3_visits}")
print()
# departments with emergency visits
emergency_departments = (final_healthcare
                         .filter(lambda row: row["visit_type"] == "Emergency")
                         .map(lambda row: row["department"])
                         .distinct()
                         )
print(f"Departments that handled emergencies: {emergency_departments.collect()}")
print()
# distinct cities and departments
print(f"Distinct Cities: {final_healthcare.map(lambda row: row["city"]).distinct().collect()}")
print(f"Distinct Departments: {final_healthcare.map(lambda row: row["department"]).distinct().collect()}")
print()
# highest average patient rating per department
avg_ratings_departments = (final_healthcare
                           .map(lambda row: (row["department"], (row["rating"], 1)))
                           .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
                           .mapValues(lambda a: round(a[0] / a[1], 2))
                           .sortBy(lambda row: row[1], ascending=False)
                           )
print(f"Average ratings by department in order: {avg_ratings_departments.collect()}")

spark.stop()