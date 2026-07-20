from pyspark.sql import SparkSession
from pathlib import Path
import csv
from pyspark.sql import functions
import os

# creating file path
data_dir = Path(__file__).parent / "data"
delivery_path = data_dir / "delivery_events.csv"
hub_path = data_dir / "hub_master.csv" 

# checking for files
try:
    if not delivery_path.is_file():
        raise FileNotFoundError("No delivery_events.csv file found.")
    if not hub_path.is_file():
        raise FileNotFoundError("No hub_master.csv file found.")
except FileNotFoundError as e:
    print(e)
    raise SystemExit # closes program quickly if file not found

# creating spark session
spark = (
    SparkSession.builder
    .appName("Day4")
    .master("local[*]")
    .getOrCreate()
)
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# load data
raw_delivery = sc.textFile(name=str(delivery_path), minPartitions=2)
raw_hub = sc.textFile(name=str(hub_path), minPartitions=2)

# print raw line count and header
print(f"Raw Delivery Events line count: {raw_delivery.count()}")
print(f"Delivery Events header: \n{raw_delivery.first()}")
print()
print(f"Raw Hub Master line count: {raw_hub.count()}")
print(f"Hub Master header: \n{raw_hub.first()}")
print()

# Remove headers and blank rows
delivery_header = raw_delivery.first()
delivery_values = raw_delivery.filter(lambda row: row != delivery_header and row != "")

hub_header = raw_hub.first()
hub_values = raw_hub.filter(lambda row: row != hub_header and row.strip() != "")

# parse records
def parse_delivery(rows):
    reader = csv.reader(rows)

    header_list = delivery_header.split(",")
    for values in reader:
        yield {
            header_list[0]: values[0].strip(),
            header_list[1]: values[1].strip(),
            header_list[2]: values[2].strip(),
            header_list[3]: values[3].strip(),
            header_list[4]: values[4].strip().upper(),
            header_list[5]: values[5].strip().upper(),
            header_list[6]: int(values[6].strip()),
            header_list[7]: int(values[7].strip()),
            header_list[8]: int(values[8].strip()),
            header_list[9]: float(values[9].strip()),
            header_list[10]: float(values[10].strip())
        }



delivery_parsed = delivery_values.mapPartitions(parse_delivery)

# validate records
valid_service_types = ["EXPRESS", "SAME_DAY", "STANDARD"]
valid_statuses = ["DELIVERED", "FAILED", "RETURNED", "IN_TRANSIT"]
def validate_delivery(row: dict):
    if row["service_type"] not in valid_service_types:
        row["class"] = "Service type not valid."
        return row
    if row["status"] not in valid_statuses:
        row["class"] = "Status not valid"
        return row
    if row["promised_hours"] <= 0 or row["actual_hours"] <= 0:
        row["class"] = "Hours not valid"
        return row
    if "" in row.values():
        row["class"] = "Element is empty"
        return row
    row["class"] = "Valid"
    return row
    
delivery_classified = delivery_parsed.map(validate_delivery).cache()

# split valid and rejected records
delivery_cleaned = delivery_classified.filter(lambda row: row["class"] == "Valid")
delivery_rejected = delivery_classified.filter(lambda row: row["class"] != "Valid")

# get only delivered shipments
delivered_shipments = delivery_cleaned.filter(lambda row: row["status"] == "DELIVERED")

# Create the Pair RDD
def pair_RDD (row):
    if row["promised_hours"] >= row["actual_hours"]:
        on_time = 1
        delay = 0
    else:
        on_time = 0
        delay = row["actual_hours"] - row["promised_hours"]

    return (row["hub_id"], (1, on_time, delay, row["delivery_charge"]))

delivered_hubs = delivered_shipments.map(pair_RDD)

# aggregate by hub
def seq_func(row1, row2):
    return (
        row1[0] + row2[0],
        row1[1] + row2[1],
        row1[2] + row2[2],
        round(row1[3] + row2[3], 2)
    )

def combo_func(row1, row2):
    return (
        row1[0] + row2[0],
        row1[1] + row2[1],
        row1[2] + row2[2],
        round(row1[3] + row2[3], 2)
    )

delivered_hubs = delivered_hubs.aggregateByKey((0, 0, 0, 0), seq_func, combo_func)

# prepare master pair RDD
def parse_hub(rows):
    reader = csv.reader(rows)

    for values in reader:
        yield (
            values[0].strip(),
            (
                values[1].strip(),
                values[2].strip(),
                values[3].strip(),
                float(values[4].strip())
            )
        )
hub_parsed = hub_values.mapPartitions(parse_hub)

# perform inner join
# both keys much match because the RDDs are joined by that key. If that key is not there, then that 
# row cannot be joined
joined_RDD = delivered_hubs.join(hub_parsed)

# calculate final KPIs
def calculate_kpis(row):
    on_time_pct = round(row[1][0][1] / row[1][0][0] * 100, 2)
    avg_delay = round(row[1][0][2] / (row[1][0][0] - row[1][0][1]), 2)
    total_charge = row[1][0][3]
    sla_gap = round((abs(row[1][1][3] - on_time_pct)), 2)
    target_status = ""
    if row[1][1][3] <= on_time_pct:
        target_status = "SUCCEED"
    else:
        target_status = "FAIL"
    return {
        "hub_id": row[0],
        "on_time_pct": on_time_pct,
        "avg_delay" : avg_delay,
        "total_charge": total_charge,
        "sla_gap": sla_gap,
        "target_status": target_status
    }

final_KPI = joined_RDD.map(calculate_kpis)

# sort
final_KPI = final_KPI.sortBy(lambda row: row["on_time_pct"], ascending=False)

# save files
save_dir = Path(__file__).parent / "output" / "generated"
hub_sla_path = save_dir / "hub_sla_report" / "hub_sla_report.csv"
rejected_delivery_events_path = save_dir / "rejected_delivery_events" / "rejected_delivery_events.csv"

os.makedirs(hub_sla_path.parent, exist_ok=True)
os.makedirs(rejected_delivery_events_path.parent, exist_ok=True)

with open(hub_sla_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=final_KPI.first().keys())

    writer.writeheader()
    final_KPI_list = final_KPI.collect()
    writer.writerows(final_KPI_list)

with open(rejected_delivery_events_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=delivery_rejected.first().keys())

    writer.writeheader()
    rejected_delivery_list = delivery_rejected.collect()
    writer.writerows(rejected_delivery_list)

hub_verify = sc.textFile(str(hub_sla_path))
rejected_verify = sc.textFile(str(rejected_delivery_events_path))

print("Final Report:")
print(hub_verify.collect())
print()
print("Rejected Rows: ")
print(rejected_verify.collect())

spark.stop()