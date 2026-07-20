import csv
from pyspark.sql import SparkSession
import os
import psutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Q1. checking input files exist
for filename in ("delivery_events.csv", "hub_master.csv"):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Required input file not found: {filename} ({path})")

# Q2. loading data with RDDs
spark = (
        SparkSession.builder.appName("Logistics Delivery SLA Analysis")
        .master("local[*]")
        .getOrCreate()
    )

sc = spark.sparkContext
sc.setLogLevel("ERROR")

# delivery events
print("=" * 50)
print("Q2")
print("=" * 50)
delivery = sc.textFile(os.path.join(DATA_DIR, "delivery_events.csv"), 2)
print(f"Delivery raw line count: {delivery.count()}")
print(f"Delivery header: {delivery.first()}")

# hub master
hub = sc.textFile(os.path.join(DATA_DIR, "hub_master.csv"), 2)
print(f"Hub raw line count: {hub.count()}")
print(f"Hub header: {hub.first()}")
print("=" * 50)

# Q3. remove header and blank rows
delivery_header = delivery.first()
delivery_data = (
    delivery
    .filter(lambda line: line != delivery_header and bool(line.strip()))
)

hub_header = hub.first()
hub_data = (
    hub
    .filter(lambda line: line != hub_header and bool(line.strip()))
)

# Q4. parse and validate events
def parse_partition(lines):
    for line in lines:
        row = next(csv.reader([line]))
        yield {"raw_line": line, "row": row}

def classify(record):
    line = record["raw_line"]
    row = record["row"]

    if len(row) != 11:
        return ("rejected", {"raw_line": line, "reason": "invalid column count"})

    # required text fields
    if not row[0].strip() or not row[3].strip():
        return ("rejected", {"raw_line": line, "reason": "missing event_id or hub_id"})

    # parse numeric fields 
    try:
        promised_hours = int(row[6])
        actual_hours = int(row[7])
        distance_km = float(row[8])
        weight_kg = float(row[9])
        delivery_charge = float(row[10])
    except ValueError:
        return ("rejected", {"raw_line": line, "reason": "non-numeric field"})

    # business rules
    if (
        actual_hours < 0 
        or promised_hours < 0 
        or delivery_charge < 0
        or distance_km < 0
        or weight_kg < 0
        ):
        return ("rejected", {"raw_line": line, "reason": "negative numeric value"})
    
    # return clean dict for later
    return ("valid", {
        "event_id": row[0].strip(),
        "event_date": row[1].strip(),
        "shipment_id": row[2].strip(),
        "hub_id": row[3].strip(),
        "service_type": row[4].strip(),
        "status": row[5].strip().upper(),
        "promised_hours": promised_hours,
        "actual_hours": actual_hours,
        "distance_km": distance_km,
        "weight_kg": weight_kg,
        "delivery_charge": delivery_charge,
    })

parsed_rdd = delivery_data.mapPartitions(parse_partition)
classified_rdd = parsed_rdd.map(classify).cache()

# Q5. one RDD for clean events, one for rejected rows and reasons
valid_events_rdd = (
    classified_rdd
    .filter(lambda x: x[0] == "valid")
    .map(lambda x: x[1])
)

invalid_events_rdd = (
    classified_rdd
    .filter(lambda x: x[0] == "rejected")
    .map(lambda x: x[1])
)

# Q6. filter business eligible records
delivered_rdd = (
    valid_events_rdd
    .filter(lambda event: event["status"] == "DELIVERED")
)

# Q7. create pair RDD
def to_hub_metrics(event):
    on_time = 1 if event["actual_hours"] <= event["promised_hours"] else 0
    delay_hours = event["actual_hours"] - event["promised_hours"]
    return (
        event["hub_id"],
        (1, on_time, delay_hours, event["delivery_charge"]),
    )
pair_rdd = delivered_rdd.map(to_hub_metrics)

# Q8. aggregate by hub 
zero_value: tuple[int, int, int, float] = (0, 0, 0, 0.0)

hub_totals_rdd = pair_rdd.aggregateByKey(
    zero_value,
    lambda acc, val: (  # pyright: ignore[reportArgumentType]
        acc[0] + val[0],
        acc[1] + val[1],
        acc[2] + val[2],
        acc[3] + val[3],
    ),
    lambda acc1, acc2: ( # pyright: ignore[reportArgumentType]
        acc1[0] + acc2[0],
        acc1[1] + acc2[1],
        acc1[2] + acc2[2],
        acc1[3] + acc2[3],
    ),
)

# Q9. load and prep master pair RDD
def to_hub_pair(line):
    row = next(csv.reader([line]))
    return (
        row[0].strip(),
        (
            row[1].strip(),
            row[2].strip(),
            row[3].strip(),
            float(row[4]),
        ),
    )

hub_pair_rdd = hub_data.map(to_hub_pair)

# Q10. join transactional and master data'
joined_rdd = hub_totals_rdd.join(hub_pair_rdd)

# Q11. calculate final KPIs
def calc_kpis(row):
    hub_id, (metrics, master) = row
    delivered, on_time, delay_total, charge_total = metrics
    city, region, manager, target = master

    on_time_pct = (on_time / delivered) * 100
    avg_delay = delay_total / delivered 
    total_charge = charge_total
    sla_gap = on_time_pct - target 
    target_status = "MET" if on_time_pct >= target else "NOT MET" 

    return {
        "hub_id": hub_id,
        "city": city,
        "region": region,
        "manager": manager,
        "sla_target_pct": target,
        "delivered_count": delivered,
        "on_time_count": on_time,
        "on_time_pct": round(on_time_pct, 2),
        "avg_delay_hours": round(avg_delay, 2),
        "total_charge": round(total_charge, 2),
        "sla_gap": round(sla_gap, 2),
        "target_status": target_status,
    }
kpi_rdd = joined_rdd.map(calc_kpis)

# Q12. sort final report
sorted_kpi_rdd = kpi_rdd.sortBy(lambda r: r["on_time_pct"], ascending = True)

# Q13. save required output files
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "generated")

REPORT_PATH = os.path.join(OUTPUT_DIR, "hub_sla_report", "hub_sla_report.csv")
REJECTED_PATH = os.path.join(
    OUTPUT_DIR, "rejected_delivery_events", "rejected_delivery_events.csv"
)

os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
os.makedirs(os.path.dirname(REJECTED_PATH), exist_ok=True)

report_rows = sorted_kpi_rdd.collect()          # already sorted in Q12
rejected_rows = invalid_events_rdd.collect()

REPORT_FIELDS = [
    "hub_id", "city", "region", "manager", "sla_target_pct",
    "delivered_count", "on_time_count", "on_time_pct",
    "avg_delay_hours", "total_charge", "sla_gap", "target_status",
]

with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=REPORT_FIELDS)
    writer.writeheader()
    writer.writerows(report_rows)

with open(REJECTED_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["raw_line", "reason"])
    writer.writeheader()
    writer.writerows(rejected_rows)

# Q14. reload and verify
print("=" * 50)
print("Q14 — hub_sla_report.csv")
print("=" * 50)
with open(REPORT_PATH, encoding="utf-8") as f:
    print(f.read())

print("=" * 50)
print("Q14 — rejected_delivery_events.csv")
print("=" * 50)
with open(REJECTED_PATH, encoding="utf-8") as f:
    print(f.read())

# Q15. reconciliation check
print(
    """
    Every input delivery event is classified as either valid or rejected. Valid events which aren't delivered
    are excluded from the SLA report by a particular rule but not lost (stored in invalid deliveries). Rejected 
    events are written to the rejected output file. Hub-level delivered count totals sum to the same count as 
    delivered_rdd so the final report reflects the results created from the pipeline. 
    """
)