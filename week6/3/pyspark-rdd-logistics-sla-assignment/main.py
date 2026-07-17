import csv
import os.path
from typing import Any

from pyspark import RDD, join
from pyspark.sql import SparkSession, metrics


def create_spark() -> SparkSession:
    spark: SparkSession = (
        SparkSession.builder.appName("rddlogisticsassignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def main():
    spark: SparkSession = create_spark()
    try:
        raw_delivery_rdd: RDD[str] = load_file(spark, "data/delivery_events.csv")
        raw_hub_rdd: RDD[str] = load_file(spark, "data/hub_master.csv")

        classified_deliveries: RDD[dict[str, Any]] = parse_deliveries_rdd(spark, raw_delivery_rdd)

        valid_deliveries_rdd: RDD[dict[str, Any]] = valid_deliveries(classified_deliveries)
        rejected_deliveries_rdd: RDD[dict[str, Any]] = rejected_deliveries(classified_deliveries)

        sla_records: RDD[dict[str, Any]] = valid_deliveries_rdd.filter(lambda row: row["status"] == "DELIVERED")

        paired_rdd: RDD[tuple[str, dict[str, Any]]] = pair_rdd(sla_records)
        aggregated_rdd: RDD[tuple[str, dict[str, Any]]] = aggregated_hub(paired_rdd)

        parsed_hub_rdd: RDD[dict[str, Any]] = parse_hub_rdd(raw_hub_rdd)
        hub_paired_rdd: RDD[tuple[str, dict[str, Any]]] = hub_pair_rdd(parsed_hub_rdd)

        #Hub id must match for the join to give proper data
        joined_rdd: RDD[tuple[str, tuple[dict[str, Any], dict[str, Any]]]] = hub_paired_rdd.join(aggregated_rdd)

        final_report: RDD[tuple[str, dict[str, Any]]] = final_report_rdd(joined_rdd)

        save_file(final_report.map(lambda x: {"hub_id": x[0], **x[1]}), "output/generated/hub_sla_report/hub_sla_report.csv")
        save_file(rejected_deliveries_rdd, "output/generated/rejected_delivery_events/rejected_delivery_events.csv")

        raw_loaded_final_report = load_file(spark, "output/generated/hub_sla_report/hub_sla_report.csv")
        raw_loaded_rejected_deliveries = load_file(spark, "output/generated/rejected_delivery_events/rejected_delivery_events.csv")

        print("Final counts vs loaded counts")
        print("Final report count:", final_report.count(), "Loaded final report count:", raw_loaded_final_report.count() - 1)
        print("Rejected deliveries count:", rejected_deliveries_rdd.count(), "Loaded rejected deliveries count:", raw_loaded_rejected_deliveries.count() - 1)

    except Exception as e:
        print(e)
        exit(1)
    finally:
        spark.stop()

def load_file(spark: SparkSession, local_path: str) -> RDD[str]:
    """
    Loads the csv file into an RDD
    :raises: FileNotFoundError when no file is found
    :param spark:
    :param local_path:
    :return:
    """
    if os.path.exists(os.path.join(os.path.dirname(__file__), local_path)):
        raw_rdd: RDD[str] = spark.sparkContext.textFile(os.path.join(os.path.dirname(__file__), local_path), 2)
        print("Loaded", local_path)
        print("Raw Count", raw_rdd.count())
        print("Header", raw_rdd.first())
        return raw_rdd
    else:
        raise FileNotFoundError(f"File not found: {local_path}")

def save_file(rdd: RDD[dict[str, Any]], local_path: str) -> None:
    """
    Saves the RDD to a CSV file
    :param rdd: RDD to save
    :param local_path: Path to save the CSV file
    """
    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    with open(local_path, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=rdd.first().keys()).writeheader()
        for row in rdd.collect():
            csv.DictWriter(f, fieldnames=row.keys()).writerow(row)

def parse_deliveries_rdd(spark: SparkSession, raw_rdd: RDD[str]) -> RDD[dict[str, Any]]:
    header: str  = raw_rdd.first()
    headers: dict[str, int] = {name: i for i, name in enumerate(header.split(","))}
    no_header: RDD[str] = raw_rdd.filter(lambda line: line != header)
    parsed_rdd: RDD[dict[str, str]] = (no_header.mapPartitions(lambda lines: ({name: line.split(",")[i] for name, i in headers.items()} for line in lines)))

    def validate(row: dict[str, Any]) -> dict[str, Any]:
        #first, coarce values:
        float_columns: set[str] = {"promised_hours","actual_hours","distance_km","weight_kg","delivery_charge"}
        for col in float_columns:
            row[col] = float(row[col])
        VALID_STATUSES: set[str] = {"DELIVERED", "IN_TRANSIT"}
        row["Valid"] = row["status"] in VALID_STATUSES
        return row

    validated_rdd: RDD[dict[str, str]] = parsed_rdd.map(validate).cache()
    return validated_rdd

def parse_hub_rdd(raw_rdd: RDD[str]) -> RDD[dict[str, Any]]:
    header: str  = raw_rdd.first()
    headers: dict[str, int] = {name: i for i, name in enumerate(header.split(","))}
    no_header: RDD[str] = raw_rdd.filter(lambda line: line != header)
    parsed_rdd: RDD[dict[str, str]] = (no_header.mapPartitions(lambda lines: ({name: line.split(",")[i] for name, i in headers.items()} for line in lines)))
    return parsed_rdd

def valid_deliveries(classified_rdd: RDD[dict[str, Any]]) -> RDD[dict[str, Any]]:
    return classified_rdd.filter(lambda row: row["Valid"])

def rejected_deliveries(classified_rdd: RDD[dict[str, Any]]) -> RDD[dict[str, Any]]:
    def rejected(row: dict[str, Any]) -> dict[str, Any]:
        rejected_reasons: dict[str, str] = {
            "FAILED": "Delivery failed for some reason",
            "RETURNED": "Delivery was returned",
            "UNKNOWN": "Unknown deliver status",
        }
        row["RejectedReason"] = rejected_reasons[row["status"]]
        return row
    return classified_rdd.filter(lambda row: not row["Valid"]).map(rejected)

def pair_rdd(sla: RDD[dict[str, Any]]) -> RDD[tuple[str, dict[str, Any]]]:
    def parse(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        metrics: dict[str, Any] = {
            "delivered_count": 1,
            "on_time": 1 if row["promised_hours"] <= row["actual_hours"] else 0,
            "delay_hours": 0 if row["promised_hours"] <= row["actual_hours"] else row["actual_hours"] - row["promised_hours"],
            "delivery_charge": row["delivery_charge"],
        }
        return row["hub_id"], metrics
    return sla.map(parse)

def aggregated_hub(pair_rdd: RDD[tuple[str, dict[str, Any]]]) -> RDD[tuple[str, dict[str, Any]]]:
    zero_value: dict[str, Any] = {
        "delivered_count": 0,
        "on_time": 0,
        "delay_hours": 0,
        "delivery_charge": 0,
    }

    def seq_op(acc: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
        return {
            "delivered_count": acc["delivered_count"] + metrics["delivered_count"],
            "on_time": acc["on_time"] + metrics["on_time"],
            "delay_hours": acc["delay_hours"] + metrics["delay_hours"],
            "delivery_charge": acc["delivery_charge"] + metrics["delivery_charge"],
        }

    def comb_op(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
        return {
            "delivered_count": a["delivered_count"] + b["delivered_count"],
            "on_time": a["on_time"] + b["on_time"],
            "delay_hours": a["delay_hours"] + b["delay_hours"],
            "delivery_charge": a["delivery_charge"] + b["delivery_charge"],
        }

    return pair_rdd.aggregateByKey(zero_value, seq_op, comb_op)

def hub_pair_rdd(parsed_hub_rdd: RDD[dict[str, Any]]) -> RDD[tuple[str, dict[str, Any]]]:
    def parse(row: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        hub_id: str = row["hub_id"]
        metrics: dict[str, Any] = {
            "city": row["hub_city"],
            "region": row["region"],
            "manager": row["manager"],
            "target": float(row["sla_target_pct"]),
        }
        return hub_id, metrics
    return parsed_hub_rdd.map(parse)


def final_report_rdd(joined_rdd: RDD[tuple[str, tuple[dict[str, Any], dict[str, Any]]]] ) -> RDD[tuple[str, dict[str, Any]]]:
    merged_rdd: RDD[tuple[str, dict[str, Any]]] = joined_rdd.mapValues(lambda x: {**x[0], **x[1]})

    def calc_final_report(row: dict[str, Any]) -> dict[str, Any]:
        row["on_time_pct"] = row["on_time"] / row ["delivered_count"] if row["delivered_count"] > 0 else 0
        row["avg_delay"] = row["delay_hours"] / row["delivered_count"] if row["delivered_count"] > 0 else 0
        row["total_charge"] = row["delivery_charge"]
        row["sla_gap"] = row["target"] - row["on_time_pct"]
        row["target_status"] = "Met" if row["on_time_pct"] >= row["target"] else "Not Met"
        return row

    return merged_rdd.mapValues(calc_final_report).sortBy(lambda x: x[1]["on_time_pct"], ascending=False)


if __name__ == "__main__":
    main()