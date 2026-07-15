import csv
from dataclasses import dataclass
import os
from typing import Any, Dict, Iterable, List, Optional

from pyspark.sql import SparkSession
import pyspark.sql.functions as F

Outage = Dict[str, Any]


@dataclass
class ValidationResult:
    is_valid: bool
    record: Optional[Outage]
    raw_line: str
    errors: List[str]


def remove_header(partition_index: int, lines: Iterable[str]) -> Iterable[str]:
    if partition_index == 0:
        next(iter(lines), None)
        lines = list(lines)

    yield from lines


def parse_and_validate_line(line: str) -> ValidationResult:
    try:
        row = next(csv.reader([line]))
        result = {}
        if len(row) != 7:
            result = {
                "is_valid": False,
                "record": None,
                "raw_line": line,
                "errors": [f"Expected 7 columns but received {len(row)}"],
            }
            return ValidationResult(**result)

        outage: Outage = {"zone": row[2].strip(), "status": row[6].strip().upper()}

        errors: List[str] = []
        if not outage["zone"]:
            errors.append("Zone is missing!")

        if not outage["status"]:
            errors.append("Status is missing!")

        allowed_statuses = {"RESOLVED", "IN_PROGRESS"}
        if outage["status"] not in allowed_statuses:
            errors.append("status must be one of RESOLVED, IN_PROGRESS")

        result = {
            "is_valid": len(errors) == 0,
            "record": outage,
            "raw_line": line,
            "errors": errors,
        }
        return ValidationResult(**result)
    except (ValueError, csv.Error) as error:
        result = {
            "is_valid": False,
            "record": None,
            "raw_line": line,
            "errors": [f"Parsing error: {error}"],
        }
        return ValidationResult(**result)


def main():
    # ----------- Part A ------------
    spark = (
        SparkSession.builder.appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    print(f"Spark version: {spark.version}")
    print(f"App name: {spark.sparkContext.appName}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
    print(f"CPU count: {os.cpu_count()}")
    print()

    # ----------- Part B ------------
    sc = spark.sparkContext
    rdd = sc.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 2)
    print(f"Partition count: {rdd.getNumPartitions()}")
    new_rdd = rdd.filter(lambda x: x > 300).map(lambda x: (x, "PEAK"))
    print(f"Peak-reading count: {new_rdd.count()}")
    print(f"First 3 peak readings: {new_rdd.take(3)}")
    print()
    """
    parallelize: Narrow Transformation
    filter: Narrow Transformation
    map: Narrow Transformation
    count: Action
    take: Action
    """
    # ----------- Part C ------------
    raw_lines_rdd = sc.textFile("./data/outages.csv")
    lines_rdd = raw_lines_rdd.mapPartitionsWithIndex(remove_header)
    validation_rdd = (
        lines_rdd.map(parse_and_validate_line)
        .cache()
        .filter(
            lambda record: (
                record.is_valid
                and record.record["zone"]  # type: ignore
                and record.record["status"] == "RESOLVED"  # type: ignore
            )
        )
    )

    final_rdd = (
        validation_rdd.map(lambda record: (record.record["zone"], int(1)))  # type: ignore
        .reduceByKey(lambda left, right: left + right)
        .sortByKey()
    )
    print(f"Resolved outage counts by zone: {final_rdd.collect()}")
    print()

    # ----------- Part D ------------
    data = [
        (201, "North", 1480.00),
        (202, "South", 925.50),
        (203, "North", 1710.25),
        (204, "East", 2480.00),
        (205, "South", 1195.75),
        (206, "Central", 3450.50),
        (207, "East", 1890.00),
        (208, "West", 1325.25),
    ]
    schema = ["bill_id", "zone", "bill_amount"]
    df = spark.createDataFrame(data=data, schema=schema)
    print(f"Dataframe: {df.collect()}")
    print()
    print(f"Schema: {df.schema}")
    print()
    stats_df = (
        df.groupBy(df.zone)
        .agg(
            F.count(df.bill_id).alias("bill_count"),
            F.round(F.sum(df.bill_amount), 2).alias("total_revenue"),
            F.round(F.avg(df.bill_amount), 2).alias("average_bill"),
        )
        .sort(F.col("total_revenue").desc())
    )
    print(f"Stats grouped by zone: {stats_df.collect()}")
    print()
    print(stats_df.explain())

    """
    HashAggregate: This operator performed groupby aggregations
    Sort: This operator sorts aggregated rows in descending order of total revenue
    """
    spark.stop()


if __name__ == "__main__":
    main()
