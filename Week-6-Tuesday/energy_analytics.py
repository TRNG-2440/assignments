import os
from pathlib import Path
from typing import cast

from pyspark import RDD
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, round, sum

DATA_DIR = Path(__file__).parent / "data"


def part_a(spark: SparkSession) -> None:
    print("=" * 60)
    print("Part A — SparkSession Runtime Inspection")
    print("=" * 60)

    sc = spark.sparkContext
    print(f"Spark version: {spark.version}")
    print(f"Application name: {spark.sparkContext.appName}")
    print(f"Master: {sc.master}")
    print(f"Default parallelism: {sc.defaultParallelism}")
    print(f"CPU count: {os.cpu_count()}")
    print()


def part_b(spark: SparkSession) -> None:
    print("=" * 60)
    print("Part B — RDD Peak Consumption Analysis")
    print("=" * 60)

    readings = [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]
    readings_rdd = spark.sparkContext.parallelize(readings, 2)

    print(f"Number of partitions: {readings_rdd.getNumPartitions()}")

    peak_rdd = readings_rdd.filter(lambda value: value >= 300).map(
        lambda value: (value, "PEAK")
    )

    print(f"Peak-reading count: {peak_rdd.count()}")
    print(f"First three peak readings: {peak_rdd.take(3)}")
    print(
        "Transformations: parallelize, filter, map, sortByKey (lazy). "
        "Actions: count, take (trigger execution)."
    )
    print()


def part_c(spark: SparkSession) -> None:
    print("=" * 60)
    print("Part C — RDD Outage Count by Zone")
    print("=" * 60)

    outages_path = (DATA_DIR / "outages.csv").as_posix()
    raw_rdd = spark.sparkContext.textFile(outages_path)
    header = raw_rdd.first()

    def parse_resolved_outage(line: str) -> tuple[str, int] | None:
        fields = line.split(",")
        if len(fields) < 7:
            return None
        zone = fields[2].strip()
        status = fields[6].strip().upper()
        if not zone or status != "RESOLVED":
            return None
        return zone, 1

    zone_counts: RDD[tuple[str, int]] = (
        raw_rdd.filter(lambda line: line != header and bool(line.strip()))
        .map(parse_resolved_outage)
        .filter(lambda record: record is not None)
        .map(lambda record: cast(tuple[str, int], record))
    )

    counts: RDD[tuple[str, int]] = zone_counts.reduceByKey(lambda a, b: a + b)
    resolved_by_zone = counts.sortByKey()  # pyright: ignore[reportCallIssue]

    print("Resolved outage counts by zone:")
    for zone, outage_count in resolved_by_zone.collect():
        print(f"{zone}: {outage_count}")
    print()


def part_d(spark: SparkSession) -> None:
    print("=" * 60)
    print("Part D — In-Memory DataFrame Billing Summary")
    print("=" * 60)

    billing_data = [
        (201, "North", 1480.00),
        (202, "South", 925.50),
        (203, "North", 1710.25),
        (204, "East", 2480.00),
        (205, "South", 1195.75),
        (206, "Central", 3450.50),
        (207, "East", 1890.00),
        (208, "West", 1325.25),
    ]

    billing_df = spark.createDataFrame(
        billing_data,
        ["bill_id", "zone", "bill_amount"],
    )

    print("Original records:")
    billing_df.show()

    print("Schema:")
    billing_df.printSchema()

    zone_report = (
        billing_df.groupBy("zone")
        .agg(
            count("bill_id").alias("bill_count"),
            round(sum("bill_amount"), 2).alias("total_revenue"),
            round(avg("bill_amount"), 2).alias("average_bill"),
        )
        .orderBy("total_revenue", ascending=False)
    )

    print("Zone billing report:")
    zone_report.show()

    print("Execution plan:")
    zone_report.explain()
    print("Plan operators identified: Aggregate and Sort.")
    print()


def main() -> None:
    spark = (
        SparkSession.builder.appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    try:
        part_a(spark)
        part_b(spark)
        part_c(spark)
        part_d(spark)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
