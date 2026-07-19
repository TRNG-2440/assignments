import os
from pathlib import Path
from pyspark.sql import SparkSession
import csv

# Q1 Input path validation
BASE_DIR = Path(__file__).resolve().parent.parent

delivery_events_path = BASE_DIR / "data" / "delivery_events.csv"
hub_master_path = BASE_DIR / "data" / "hub_master.csv"

if not delivery_events_path.exists():
    raise FileNotFoundError(
        f"Input file not found: {delivery_events_path}. "
        "Expected shipment-event data at data/delivery_events.csv"
    )

if not hub_master_path.exists():
    raise FileNotFoundError(
        f"Input file not found: {hub_master_path}. "
        "Expected hub master data at data/hub_master.csv"
    )

print(f"[Q1] Input files verified:\n  {delivery_events_path}\n  {hub_master_path}")

# Q2 Load data using RDDs
spark = (
    SparkSession.builder
    .appName("Assignment 4")
    .master("local[*]")
    .getOrCreate()
)

sc = spark.sparkContext 

de_rdd = sc.textFile(str(delivery_events_path), minPartitions=4)
hm_rdd = sc.textFile(str(hub_master_path), minPartitions=4)

de_header = de_rdd.first()
hm_header = hm_rdd.first()

print("\n[Q2] delivery_events RDD sample:")
print(f"Total records (including header): {de_rdd.count()}")
print(f"Header line: {de_header}")

print("\nhub_master RDD sample:")
print(f"Total records (including header): {hm_rdd.count()}")
print(f"Header line: {hm_header}")

# Q3 Remove headers and blank rows
data_de_rdd = de_rdd.filter(lambda line: line != de_header and bool(line.strip()))
data_hm_rdd = hm_rdd.filter(lambda line: line != hm_header and bool(line.strip()))

print(f"\n[Q3] Delivery events data: {data_de_rdd.take(3)}")
print(f"\nHub master data: {data_hm_rdd.take(3)}")

# Q4 Parse and validate events
def parse_partition(rows):
    for row in rows:
        cols = [c.strip() for c in row.split(",")]

        if len(cols) != 11:
            yield {
                "_raw": row,
                "_parse_error": "Wrong column count"
            }
            continue

        yield {
            "event_id": cols[0],
            "event_date": cols[1],
            "shipment_id": cols[2],
            "hub_id": cols[3],
            "service_type": cols[4],
            "status": cols[5].upper(),
            "promised_hours": cols[6],
            "actual_hours": cols[7],
            "distance_km": cols[8],
            "weight_kg": cols[9],
            "delivery_charge": cols[10],
            "_raw": row
        }

parsed_events = data_de_rdd.mapPartitions(parse_partition)

def classify(event):
    if "_parse_error" in event:
        return (
            "REJECTED",
            {
                "raw_line": event["_raw"],
                "reason": event["_parse_error"]
            }
        )

    try:
        # Required field checks
        if (
            event["event_id"] == "" or
            event["shipment_id"] == "" or
            event["hub_id"] == "" or
            event["status"] == ""
        ):
            return (
                "REJECTED",
                {
                    "raw_line": event["_raw"],
                    "reason": "Missing required field"
                }
            )

        # Numeric validation + conversion
        event["promised_hours"] = float(event["promised_hours"])
        event["actual_hours"] = float(event["actual_hours"])
        event["distance_km"] = float(event["distance_km"])
        event["weight_kg"] = float(event["weight_kg"])
        event["delivery_charge"] = float(event["delivery_charge"])

        return ("VALID", event)

    except ValueError:
        return (
            "REJECTED",
            {
                "raw_line": event["_raw"],
                "reason": "Invalid numeric value"
            }
        )


classified_events = parsed_events.map(classify).cache()

print("\n[Q4] Sample classified records:")
for row in classified_events.take(10):
    print(row)

print("[Q4] Valid count:", classified_events.filter(lambda x: x[0] == "VALID").count())
print("[Q4] Rejected count:", classified_events.filter(lambda x: x[0] == "REJECTED").count())

# Q5 Split valid and rejected records
valid_events_rdd = (
    classified_events
    .filter(lambda x: x[0] == "VALID")
    .map(lambda x: x[1])
)

rejected_events_rdd = (
    classified_events
    .filter(lambda x: x[0] == "REJECTED")
    .map(lambda x: x[1])
)

print("\n[Q5] Valid events sample:")
for row in valid_events_rdd.take(5):
    print(row)

print("\n[Q5] Rejected events sample:")
for row in rejected_events_rdd.take(5):
    print(row)

print("[Q5] Valid count:", valid_events_rdd.count())
print("[Q5] Rejected count:", rejected_events_rdd.count())

# Q6 Filter business-eligible records
delivered_events_rdd = valid_events_rdd.filter(lambda event: event["status"] == "DELIVERED")

print("[Q6] Delivered count:", delivered_events_rdd.count())

# Q7 Create the Pair RDD
def make_hubs_metric_pair(event):
    hub_id = event["hub_id"]

    if not hub_id:
        hub_id = "UNKNOWN"

    promised = event["promised_hours"]
    actual = event["actual_hours"]
    charge = event["delivery_charge"]

    if actual <= promised:
        on_time = 1
        delay_hours = 0.0
    else:
        on_time = 0
        delay_hours = actual - promised

    return (
        hub_id,
        {
            "delivered_count": 1,
            "on_time_count": on_time,
            "delay_hours_sum": delay_hours,
            "delivery_charge_sum": charge,
        },
    )

hub_metrics_rdd = delivered_events_rdd.map(make_hubs_metric_pair)

print("\n[Q7] Sample per-event hub metrics:")
for row in hub_metrics_rdd.take(5):
    print(row)

# Q8 Aggregate by hub
zero_value = {
    "delivered_count": 0,
    "on_time_count": 0,
    "delay_hours_sum": 0.0,
    "delivery_charge_sum": 0.0,
}

def seq_op(acc, metrics):
    return {
        "delivered_count": acc["delivered_count"] + metrics["delivered_count"],
        "on_time_count": acc["on_time_count"] + metrics["on_time_count"],
        "delay_hours_sum": acc["delay_hours_sum"] + metrics["delay_hours_sum"],
        "delivery_charge_sum": acc["delivery_charge_sum"] + metrics["delivery_charge_sum"],
    }

def comb_op(acc1, acc2):
    return {
        "delivered_count": acc1["delivered_count"] + acc2["delivered_count"],
        "on_time_count": acc1["on_time_count"] + acc2["on_time_count"],
        "delay_hours_sum": acc1["delay_hours_sum"] + acc2["delay_hours_sum"],
        "delivery_charge_sum": acc1["delivery_charge_sum"] + acc2["delivery_charge_sum"],
    }

hub_totals_rdd = hub_metrics_rdd.aggregateByKey(zero_value, seq_op, comb_op)

print("\n[Q8] Aggregated hub totals:")
for row in hub_totals_rdd.collect():
    print(row)

# Q9 Load and prepare the master Pair RDD

def parse_hub_master_line(line):
    cols = [c.strip() for c in line.split(",")]

    if len(cols) != 5:
        return ("UNKNOWN", ("UNKNOWN", "UNKNOWN", "UNKNOWN", 0.0))

    hub_id, hub_city, region, manager, sla_target_pct = cols

    try:
        target_pct = float(sla_target_pct)
    except ValueError:
        target_pct = 0.0
    return (
        hub_id,
        (hub_city, region, manager, target_pct)
    )

hub_master_pair_rdd = data_hm_rdd.map(parse_hub_master_line)

print("\n[Q9] Hub master Pair RDD sample:")
for row in hub_master_pair_rdd.take(5):
    print(row)

# Q10 Join transactional and master data
joined_rdd = hub_totals_rdd.join(hub_master_pair_rdd)

def build_joined_record(item):
    hub_id, (metrics, master) = item
    hub_city, region, manager, sla_target_pct = master

    return {
        "hub_id": hub_id,
        "hub_city": hub_city,
        "region": region,
        "manager": manager,
        "delivered_count": metrics["delivered_count"],
        "on_time_count": metrics["on_time_count"],
        "delay_hours_sum": metrics["delay_hours_sum"],
        "delivery_charge_sum": metrics["delivery_charge_sum"],
        "sla_target_pct": sla_target_pct,
    }


joined_records_rdd = joined_rdd.map(build_joined_record)

print("\n[Q10] Joined records:")
for row in joined_records_rdd.take(5):
    print(row)
print("Keys must match so that a proper inner join between the two rdds are possible. Different keys would not allow for a join to work.")

# Q11 Calculate final KPIs

def add_kpis(record):
    delivered = record["delivered_count"]
    on_time = record["on_time_count"]
    delay_sum = record["delay_hours_sum"]
    total_charge = record["delivery_charge_sum"]
    target_pct = record["sla_target_pct"]

    if delivered > 0:
        on_time_pct = (on_time / delivered) * 100.0
        avg_delay_hours = delay_sum / delivered
    else:
        on_time_pct = 0.0
        avg_delay_hours = 0.0

    sla_gap = on_time_pct - target_pct

    target_status = "MET" if on_time_pct >= target_pct else "MISS"

    result = dict(record)
    result.update({
        "on_time_pct": on_time_pct,
        "avg_delay_hours": avg_delay_hours,
        "total_charge": total_charge,
        "sla_gap": sla_gap,
        "target_status": target_status,
    })
    return result


kpi_rdd = joined_records_rdd.map(add_kpis)

print("\n[Q11] Hub KPIs sample:")
for row in kpi_rdd.take(5):
    print(row)

# Q12 Sort the final report
sorted_kpi_rdd = kpi_rdd.sortBy(
    keyfunc=lambda rec: rec["on_time_pct"],
    ascending=False
)

print("\n[Q12] Sorted hub SLA report (top 5):")
for row in sorted_kpi_rdd.take(5):
    print(row)

# Q13 Save the required output files
# Output directories
hub_report_dir = BASE_DIR / "output" / "generated" / "hub_sla_report"
rejected_dir = BASE_DIR / "output" / "generated" / "rejected_delivery_events"

# Create directories if they do not exist
hub_report_dir.mkdir(parents=True, exist_ok=True)
rejected_dir.mkdir(parents=True, exist_ok=True)

# Output file paths
hub_report_path = hub_report_dir / "hub_sla_report.csv"
rejected_path = rejected_dir / "rejected_delivery_events.csv"

# Collect small final results
hub_report_rows = sorted_kpi_rdd.collect()
rejected_rows = rejected_events_rdd.collect()

hub_report_fields = [
    "hub_id",
    "hub_city",
    "region",
    "manager",
    "delivered_count",
    "on_time_count",
    "delay_hours_sum",
    "delivery_charge_sum",
    "sla_target_pct",
    "on_time_pct",
    "avg_delay_hours",
    "total_charge",
    "sla_gap",
    "target_status",
]

with open(hub_report_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=hub_report_fields)
    writer.writeheader()
    for row in hub_report_rows:
        writer.writerow(row)

print(f"\n[Q13] Saved hub SLA report to: {hub_report_path}")

# Save rejected delivery events
with open(rejected_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["raw_line", "reason"])
    for row in rejected_rows:
        writer.writerow([
            row.get("raw_line", ""),
            row.get("reason", "")
        ])

print(f"[Q13] Saved rejected delivery events to: {rejected_path}")

# Q14 Reload and verify saved output
print("\n[Q14] Reloaded hub SLA report:")
with hub_report_path.open(mode="r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

print("\n[Q14] Reloaded rejected delivery events:")
with rejected_path.open(mode="r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    # skip header row
    header = next(reader, None)
    print("Header:", header)
    for row in reader:
        print(row)

# Q15 Reconciliation check
total_input_events = data_de_rdd.count()
total_valid = valid_events_rdd.count()
total_rejected = rejected_events_rdd.count()

print("\n[Q15] Reconciliation check:")
print("Total input events (after header/blank removal):", total_input_events)
print("Total VALID events:", total_valid)
print("Total REJECTED events:", total_rejected)
print("VALID + REJECTED:", total_valid + total_rejected)

if total_input_events == total_valid + total_rejected:
    print("[Q15] PASS - all input records accounted for (no silent loss).")
else:
    print("[Q15] FAIL - mismatch detected, some records may have been lost.")

spark.stop()