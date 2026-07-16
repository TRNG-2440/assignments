import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def section(title):
    print("=" * 90)
    print(title)
    print("=" * 90)


def part_a():
    section("PART A: SparkSession Runtime Inspection")

    spark = (
        SparkSession.builder
        .appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    sc = spark.sparkContext
    print(f"Spark version: {spark.version}")
    print(f"Application name: {sc.appName}")
    print(f"Master: {sc.master}")
    print(f"Default parallelism: {sc.defaultParallelism}")
    print(f"CPU count: {os.cpu_count()}")

    return spark


def part_b(spark):
    section("PART B: RDD Peak Consumption Analysis")

    sc = spark.sparkContext
    readings = [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]

    readings_rdd = sc.parallelize(readings, 2)
    print(f"Number of partitions       : {readings_rdd.getNumPartitions()}")

    peak_rdd = readings_rdd.filter(lambda r: r >= 300)

    tagged_peak_rdd = peak_rdd.map(lambda r: (r, "PEAK"))

    peak_count = tagged_peak_rdd.count()
    print(f"Peak reading count (>=300) : {peak_count}")

    first_three_peaks = tagged_peak_rdd.take(3)
    print(f"First three peak readings  : {first_three_peaks}")

    print(
        "transformations used: parallelize(), filter(), map()\n"
        "actions used: count(), take()"
    )

    return tagged_peak_rdd


def part_c(spark):
    section("PART C: RDD Outage Count by Zone")

    sc = spark.sparkContext
    raw_rdd = sc.textFile(os.path.join(DATA_DIR, "outages.csv"))

    header = raw_rdd.first()
    data_rdd = raw_rdd.filter(lambda row: row != header)

    def parse_zone_status(row):
        cols = row.split(",")
        zone = cols[2].strip() if len(cols) > 2 else ""
        status = cols[6].strip().upper() if len(cols) > 6 else ""
        return (zone, status)

    parsed_rdd = data_rdd.map(parse_zone_status)

    resolved_rdd = parsed_rdd.filter(
        lambda z_s: z_s[0] != "" and z_s[1] == "RESOLVED"
    )

    zone_counts_rdd = resolved_rdd.map(lambda z_s: (z_s[0], 1)) \
        .reduceByKey(lambda a, b: a + b)

    sorted_result = zone_counts_rdd.sortByKey().collect()

    print("Resolved outage count by zone (alphabetical):")
    for zone, cnt in sorted_result:
        print(f"  {zone:<10} -> {cnt}")

    return sorted_result


def part_d(spark):
    section("PART D: In-Memory DataFrame Billing Summary")

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
    bills_df = spark.createDataFrame(data, ["bill_id", "zone", "bill_amount"])

    print("Original records:")
    bills_df.show()

    print("Schema:")
    bills_df.printSchema()

    billing_summary_df = (
        bills_df.groupBy("zone")
        .agg(
            F.count("bill_id").alias("bill_count"),
            F.sum("bill_amount").alias("total_revenue"),
            F.avg("bill_amount").alias("average_bill"),
        )
        .withColumn("total_revenue", F.round("total_revenue", 2))
        .withColumn("average_bill", F.round("average_bill", 2))
        .orderBy(F.col("total_revenue").desc())
    )

    print("Billing summary by zone (ordered by total revenue desc):")
    billing_summary_df.show()

    print("Execution plan (explain()):")
    billing_summary_df.explain()

    print(
        "Identified plan operations: groupBy(), agg(), withColumn(), orderBy()"
    )

    return billing_summary_df


def main():
    spark = part_a()
    try:
        part_b(spark)
        part_c(spark)
        part_d(spark)
    finally:
        section("Stopping SparkSession")
        spark.stop()
        print("SparkSession stopped.")


if __name__ == "__main__":
    main()

