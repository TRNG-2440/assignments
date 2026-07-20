from pyspark.sql import SparkSession
from pathlib import Path
import csv
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


# Build a PySpark RDD pipeline that loads shipment-event and hub-master CSV files, 
# validates rows, separates rejected events, calculates delivery SLA KPIs by hub, 
# joins the result with hub master data, sorts the report, and saves final CSV files.

BASE_DIR = Path(__file__).resolve().parent
EVENT_FILE = BASE_DIR / "data" / "delivery_events.csv"
MASTER_FILE = BASE_DIR / "data" / "hub_master.csv"

REPORT_OUTPUT = (
    BASE_DIR /
    "output/generated/hub_sla_report/hub_sla_report.csv"
)

REJECT_OUTPUT = (
    BASE_DIR /
    "output/generated/rejected_delivery_events/rejected_delivery_events.csv"
)

if not EVENT_FILE.exists():
    raise FileNotFoundError(
        f"Missing input file: {EVENT_FILE}"
    )
if not MASTER_FILE.exists():
    raise FileNotFoundError(
        f"Missing input file: {MASTER_FILE}"
    )

def main() -> None:
    spark = (
        SparkSession.builder.appName("Shipment SLA Pipeline")
        .master("local[*]")
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    event_rdd = sc.textFile(str(EVENT_FILE), minPartitions=2)
    master_rdd = sc.textFile(str(MASTER_FILE), minPartitions=2)

   
    print(f"\nDelivery rows before cleaning: {event_rdd.count()}")
    print(event_rdd.first())
    print(f"\nMaster rows before cleaning: {master_rdd.count()}")
    print(master_rdd.first())

    event_header = event_rdd.first()
    master_header = master_rdd.first()

    event_rdd = event_rdd.filter(lambda x: x != event_header)
    master_rdd = master_rdd.filter(lambda x: x != master_header)
    event_rdd = event_rdd.filter(lambda x: x.strip() !="")
    master_rdd = master_rdd.filter(lambda x: x.strip() !="")

    print(f"\nDelivery rows after cleaning: {event_rdd.count()}")
    print("First 3 rows:")
    for line in event_rdd.take(3): 
        print(line) 
    print(f"\nMaster rows after cleaning:  {master_rdd.count()}")
    print("First 3 rows: ")
    for line in master_rdd.take(3):
        print(line)

    def parse_partition(iterator):
        for line in iterator:

            fields = line.split(",")

            yield {
                "event_id": fields[0],
                "event_date": fields[1],
                "shipment_id": fields[2],
                "hub_id": fields[3],
                "service_type": fields[4],
                "status": fields[5],
                "promised_hours": int(fields[6]),
                "actual_hours": int(fields[7]),
                "distance_km": int(fields[8]),
                "weight_kg": float(fields[9]),
                "delivery_charge": float(fields[10]),
            }

    event_rdd = event_rdd.mapPartitions(parse_partition)
    print("\n ===PARSED===")
    print(event_rdd.first())
    
    def validate(record):
        reason = None

        if record["delivery_charge"] <= 0:
            reason = "Invalid delivery charge"

        elif record["promised_hours"] <= 0:
            reason = "Invalid promised hours"

        elif record["actual_hours"] <= 0:
            reason = "Invalid actual hours"
        
        elif record["hub_id"] == "":
            reason = "Invalid hub id"
        
        if reason:
            return {
                "valid": False,
                "reason": reason,
                "record": record
            }

        return {
            "valid": True,
            "reason": None,
            "record": record
        }
    classified_rdd = event_rdd.map(validate)
    classified_rdd.cache()
    print("\n ===CLASSIFIED===")
    for line in classified_rdd.take(3):
        print(line)

    valid_rdd = classified_rdd \
        .filter(lambda x: x["valid"]) \
        .map(lambda x: x["record"])


    rejected_rdd = classified_rdd \
        .filter(lambda x: not x["valid"])


    valid_count = valid_rdd.count()
    rejected_count = rejected_rdd.count()

    print("\n ===VALID/REJECTED COUNT===")
    print(f"Valid: {valid_count}")
    print(f"Rejected: {rejected_count}")

    delivered_rdd = valid_rdd.filter(
        lambda x: x["status"] == "DELIVERED"
    )

    delivered_rdd.cache()
    print("\n ===DELIVERED COUNT/FIRST THREE===")
    print(f"Delivered: {delivered_rdd.count()}")
    for line in delivered_rdd.take(3):
        print(line)

    hub_metrics_rdd = delivered_rdd.map(
        lambda x: (
            x["hub_id"],
            {
                "delivered_count": 1,
                "on_time_count": 
                    1 if x["actual_hours"] <= x["promised_hours"] else 0,
                "delay_hours":
                    max(x["actual_hours"] - x["promised_hours"], 0),
                "delivery_charge":
                    x["delivery_charge"]
            }
        )
    )

    hub_metrics = hub_metrics_rdd.aggregateByKey(
        {
            "delivered_count": 0,
            "on_time_count": 0,
            "delay_hours": 0,
            "delivery_charge": 0
        },

        lambda acc, value: {

            "delivered_count":
                acc["delivered_count"] + value["delivered_count"],

            "on_time_count":
                acc["on_time_count"] + value["on_time_count"],

            "delay_hours":
                acc["delay_hours"] + value["delay_hours"],

            "delivery_charge":
                acc["delivery_charge"] + value["delivery_charge"]
        },

        lambda a, b: {

            "delivered_count":
                a["delivered_count"] + b["delivered_count"],

            "on_time_count":
                a["on_time_count"] + b["on_time_count"],

            "delay_hours":
                a["delay_hours"] + b["delay_hours"],

            "delivery_charge":
                a["delivery_charge"] + b["delivery_charge"]
        }
    )

    print("\n ===HUB METRICS===")
    for line in hub_metrics.collect():
        print(line)

    hub_report_rdd = hub_metrics.map(
        lambda x: (
            x[0],
            {
                "total_deliveries": x[1]["delivered_count"],

                "on_time_pct": round(
                    (
                        x[1]["on_time_count"]
                        /
                        x[1]["delivered_count"]
                    ) * 100,
                    2
                ),

                "avg_delay": round(
                    x[1]["delay_hours"]
                    /
                    x[1]["delivered_count"],
                    2
                ),

                "total_charge": round(
                    x[1]["delivery_charge"],
                    2
                )
            }
        )
    )

    print("\n ===HUB REPORT===")
    for line in hub_report_rdd.collect():
        print(line)

    def parse_master(iterator):
        for line in iterator:
            fields = line.split(",")
            yield {
            "hub_id": fields[0],
            "hub_city": fields[1],
            "region": fields[2],
            "manager": fields[3],
            "sla_target_pct": float(fields[4])
        }

    master_rdd = master_rdd.mapPartitions(parse_master)
    print("\n ===PARSED MASTER===")
    for line in master_rdd.take(3):
        print(line)
    
    master_pair_rdd = master_rdd.map(
        lambda x: (
            x["hub_id"],
            (
                x["hub_city"],
                x["region"],
                x["manager"],
                x["sla_target_pct"]
            )
        )
    )
    
    joined_rdd = hub_report_rdd.join(master_pair_rdd)
    print("\n ===HUB REPORT JOINED===")
    for row in joined_rdd.take(5):
        print(row)
    
    final_report_rdd = joined_rdd.map(
        lambda x: {
            "hub_id": x[0],
            "city": x[1][1][0],
            "region": x[1][1][1],
            "manager": x[1][1][2],

            "delivered_count": x[1][0]["total_deliveries"],

            "on_time_pct": x[1][0]["on_time_pct"],

            "avg_delay": x[1][0]["avg_delay"],

            "total_charge": x[1][0]["total_charge"],

            "sla_gap": round(
                x[1][0]["on_time_pct"] - x[1][1][3],
                2
            ),

            "target_status":
                "MET"
                if x[1][0]["on_time_pct"] >= x[1][1][3]
                else "NOT MET"
        }
    )
    
    final_report_rdd.cache()
    for row in hub_metrics.collect():
        print(row)
    
      
    print("\n ===FINAL REPORT===")
    for line in final_report_rdd.take(3):
        print(line)
    
    sorted_report_rdd = final_report_rdd.sortBy(
        lambda x: x["on_time_pct"],
        ascending=False
    )
    
    print("\n ===SORTED FINAL REPORT===")
    final_report = sorted_report_rdd.collect()
    for line in final_report:
        print(line)

    reject_records = rejected_rdd.map(
        lambda x: {
            **x["record"],
            "reason": x["reason"]
        }
    ).collect()

    print("\n ===REJECTED RECORDS===")
    for line in reject_records:
        print(line)

    REPORT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    REJECT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_OUTPUT, 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=final_report[0].keys())
        writer.writeheader()
        writer.writerows(final_report)

    with open(REJECT_OUTPUT, 'w', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=reject_records[0].keys())
        writer.writeheader()
        writer.writerows(reject_records)

    print("\n ==HUB SLA REPORT===")
    with open(REPORT_OUTPUT, "r") as f:
        print(f.read())

    print("\n ==REJECTED RECORDS===")
    with open(REJECT_OUTPUT, "r") as f:
        print(f.read())


    raw_records = event_rdd.count()

    valid_records = valid_rdd.count()

    rejected_records_count = rejected_rdd.count()

    delivered_records = delivered_rdd.count()
    
    
    print("\n=== RECONCILIATION ===")
    print(f"Input records:      {raw_records}")
    print(f"Valid records:      {valid_records}")
    print(f"Rejected records:   {rejected_records_count}")
    print(f"Delivered records:  {delivered_records}")
    print(f"Non-delivered:      {valid_records - delivered_records}")

    print(
        f"Check: {raw_records} == "
        f"{valid_records + rejected_records_count}"
    )   

    if raw_records == valid_records + rejected_records_count:
        print("PASS: No records were lost.")
    else:
        print("FAIL: Record count mismatch!")
        

    spark.stop()

if __name__ == "__main__":
    main()