import csv
from dataclasses import dataclass
import os
from typing import Any, Dict, Iterable, Iterator, List, Optional

from pyspark.sql import SparkSession

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

    sc = spark.sparkContext
    rdd = sc.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 2)
    print(f"Partition count: {rdd.getNumPartitions()}")
    new_rdd = rdd.filter(lambda x: x > 300).map(lambda x: (x, "PEAK"))
    print(f"Peak-reading count: {new_rdd.count()}")
    print(f"First 3 peak readings: {new_rdd.take(3)}")
    """
    parallelize: Narrow Transformation
    filter: Narrow Transformation
    map: Narrow Transformation
    count: Action
    take: Action
    """

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
    spark.stop()


if __name__ == "__main__":
    main()
