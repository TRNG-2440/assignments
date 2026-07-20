from __future__ import annotations

import csv
from datetime import date
from pathlib import Path
from typing import Iterable, Iterator

from pyspark import SparkContext
from pyspark.sql import SparkSession


PROJECT_DIR = Path(__file__).resolve().parents[1]
EVENTS_PATH = PROJECT_DIR / "data" / "delivery_events.csv"
HUBS_PATH = PROJECT_DIR / "data" / "hub_master.csv"
REPORT_PATH = (
    PROJECT_DIR / "output" / "generated" / "hub_sla_report" / "hub_sla_report.csv"
)
REJECTED_PATH = (
    PROJECT_DIR
    / "output"
    / "generated"
    / "rejected_delivery_events"
    / "rejected_delivery_events.csv"
)

EVENT_COLUMNS = [
    "event_id",
    "event_date",
    "shipment_id",
    "hub_id",
    "service_type",
    "status",
    "promised_hours",
    "actual_hours",
    "distance_km",
    "weight_kg",
    "delivery_charge",
]

REPORT_COLUMNS = [
    "hub_id",
    "hub_city",
    "region",
    "manager",
    "sla_target_pct",
    "delivered_count",
    "on_time_count",
    "on_time_pct",
    "avg_delay_hours",
    "total_delivery_charge",
    "sla_gap",
    "target_status",
]

VALID_STATUSES = {"DELIVERED", "IN_TRANSIT", "RETURNED", "FAILED"}
VALID_SERVICE_TYPES = {"STANDARD", "EXPRESS", "SAME_DAY"}


def validate_input_paths(*paths: Path) -> None:
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Required input file was not found: {path}")


def parse_event_partition(lines: Iterable[str]) -> Iterator[dict]:
    for line in lines:
        try:
            values = next(csv.reader([line]))
            yield {"raw_row": line, "values": values, "parse_error": ""}
        except (csv.Error, StopIteration) as error:
            yield {
                "raw_row": line,
                "values": [],
                "parse_error": f"CSV parse error: {error}",
            }


def classify_event(parsed: dict) -> tuple[str, dict]:
    reasons = []
    values = parsed["values"]

    if parsed["parse_error"]:
        reasons.append(parsed["parse_error"])

    if len(values) != len(EVENT_COLUMNS):
        reasons.append(f"expected {len(EVENT_COLUMNS)} columns, got {len(values)}")
        record = {}
    else:
        record = {
            column: value.strip() for column, value in zip(EVENT_COLUMNS, values)
        }

    if record:
        for column in EVENT_COLUMNS:
            if not record[column]:
                reasons.append(f"{column} is required")

        try:
            date.fromisoformat(record["event_date"])
        except ValueError:
            reasons.append("event_date must use YYYY-MM-DD format")

        if record["status"] not in VALID_STATUSES:
            reasons.append(f"invalid status: {record['status']}")

        if record["service_type"] not in VALID_SERVICE_TYPES:
            reasons.append(f"invalid service_type: {record['service_type']}")

        numeric_values = {}
        for column in [
            "promised_hours",
            "actual_hours",
            "distance_km",
            "weight_kg",
            "delivery_charge",
        ]:
            try:
                numeric_values[column] = float(record[column])
            except ValueError:
                reasons.append(f"{column} must be numeric")

        if "promised_hours" in numeric_values and numeric_values["promised_hours"] <= 0:
            reasons.append("promised_hours must be greater than zero")
        if "actual_hours" in numeric_values and numeric_values["actual_hours"] < 0:
            reasons.append("actual_hours cannot be negative")
        if "distance_km" in numeric_values and numeric_values["distance_km"] <= 0:
            reasons.append("distance_km must be greater than zero")
        if "weight_kg" in numeric_values and numeric_values["weight_kg"] <= 0:
            reasons.append("weight_kg must be greater than zero")
        if "delivery_charge" in numeric_values and numeric_values["delivery_charge"] < 0:
            reasons.append("delivery_charge cannot be negative")

    if reasons:
        return "rejected", {
            "raw_row": parsed["raw_row"],
            "rejection_reason": "; ".join(reasons),
        }

    clean_record = dict(record)
    clean_record.update(numeric_values)
    return "valid", clean_record


def to_hub_metric(event: dict) -> tuple[str, tuple[int, int, float, float]]:
    on_time = int(event["actual_hours"] <= event["promised_hours"])
    delay = max(event["actual_hours"] - event["promised_hours"], 0.0)
    metrics = (1, on_time, delay, event["delivery_charge"])
    return event["hub_id"], metrics


def add_metrics(
    left: tuple[int, int, float, float],
    right: tuple[int, int, float, float],
) -> tuple[int, int, float, float]:
    return tuple(a + b for a, b in zip(left, right))


def parse_hub_line(line: str) -> tuple[str, tuple[str, str, str, float]]:
    hub_id, city, region, manager, target = next(csv.reader([line]))
    return hub_id, (city, region, manager, float(target))


def calculate_kpis(joined_item: tuple[str, tuple[tuple, tuple]]) -> dict:
    hub_id, (totals, master) = joined_item
    delivered_count, on_time_count, total_delay, total_charge = totals
    city, region, manager, target = master

    on_time_pct = round(on_time_count / delivered_count * 100, 2)
    avg_delay_hours = round(total_delay / delivered_count, 2)
    sla_gap = round(on_time_pct - target, 2)
    target_status = "MET" if on_time_pct >= target else "MISSED"

    return {
        "hub_id": hub_id,
        "hub_city": city,
        "region": region,
        "manager": manager,
        "sla_target_pct": target,
        "delivered_count": delivered_count,
        "on_time_count": on_time_count,
        "on_time_pct": on_time_pct,
        "avg_delay_hours": avg_delay_hours,
        "total_delivery_charge": round(total_charge, 2),
        "sla_gap": sla_gap,
        "target_status": target_status,
    }


def write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def print_saved_file(path: Path) -> None:
    with path.open("r", encoding="utf-8") as file:
        print(f"\n{path}\n{file.read()}")


def build_pipeline(sc: SparkContext) -> None:
    raw_events = sc.textFile(str(EVENTS_PATH), minPartitions=2)
    raw_hubs = sc.textFile(str(HUBS_PATH), minPartitions=2)

    event_header = raw_events.first()
    hub_header = raw_hubs.first()
    print(f"Raw event line count: {raw_events.count()}")
    print(f"Event header: {event_header}")
    print(f"Raw hub line count: {raw_hubs.count()}")
    print(f"Hub header: {hub_header}")

    event_lines = raw_events.filter(
        lambda line: bool(line.strip()) and line != event_header
    )
    hub_lines = raw_hubs.filter(lambda line: bool(line.strip()) and line != hub_header)

    classified = event_lines.mapPartitions(parse_event_partition).map(
        classify_event
    ).cache()

    valid_events = classified.filter(lambda item: item[0] == "valid").map(
        lambda item: item[1]
    )
    rejected_events = classified.filter(lambda item: item[0] == "rejected").map(
        lambda item: item[1]
    )

    eligible_events = valid_events.filter(lambda event: event["status"] == "DELIVERED")
    hub_metrics = eligible_events.map(to_hub_metric)

    hub_totals = hub_metrics.aggregateByKey(
        (0, 0, 0.0, 0.0),
        add_metrics,
        add_metrics,
    )

    hub_master = hub_lines.map(parse_hub_line)
    joined = hub_totals.join(hub_master)

    final_report = joined.map(calculate_kpis).sortBy(
        lambda row: row["on_time_pct"], ascending=False
    )

    report_rows = final_report.collect()
    rejected_rows = rejected_events.collect()

    write_csv(REPORT_PATH, REPORT_COLUMNS, report_rows)
    write_csv(
        REJECTED_PATH,
        ["raw_row", "rejection_reason"],
        rejected_rows,
    )

    print_saved_file(REPORT_PATH)
    print_saved_file(REJECTED_PATH)

    input_count = event_lines.count()
    rejected_count = len(rejected_rows)
    valid_count = valid_events.count()
    delivered_count = eligible_events.count()
    non_delivered_count = valid_count - delivered_count
    reported_delivered_count = int(
        joined.map(lambda item: item[1][0][0]).sum()
    )
    missing_master_count = int(
        hub_totals.leftOuterJoin(hub_master)
        .filter(lambda item: item[1][1] is None)
        .map(lambda item: item[1][0][0])
        .sum()
    )

    assert input_count == valid_count + rejected_count
    assert valid_count == delivered_count + non_delivered_count
    assert delivered_count == reported_delivered_count + missing_master_count
    assert input_count == (
        rejected_count
        + non_delivered_count
        + reported_delivered_count
        + missing_master_count
    )

    print("\nReconciliation passed")
    print(f"Input records: {input_count}")
    print(f"Rejected records: {rejected_count}")
    print(f"Valid non-delivered records: {non_delivered_count}")
    print(f"Reported delivered records: {reported_delivered_count}")
    print(f"Delivered records without a matching hub: {missing_master_count}")

    classified.unpersist()


def main() -> None:
    validate_input_paths(EVENTS_PATH, HUBS_PATH)

    spark = (
        SparkSession.builder.master("local[*]")
        .appName("LogisticsDeliverySLA")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    try:
        build_pipeline(spark.sparkContext)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
