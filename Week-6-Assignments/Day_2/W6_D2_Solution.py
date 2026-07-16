from pyspark.sql import SparkSession, functions as F
import os

print("------- Part A -------")
spark = (
    SparkSession.builder
    .appName("EnergyUtilityAssignment")
    .master("local[*]")
    .getOrCreate()
    )

spark.sparkContext.setLogLevel("ERROR")

print("Spark Version: ", spark.version)
print("Application Name: ", spark.sparkContext.appName)
print("Master: ", spark.sparkContext.master)
print("Default Parallelism: ", spark.sparkContext.defaultParallelism)
print("CPU Count: ", os.cpu_count())

# spark.stop()

print("------- Part B -------")

numbers_rdd = spark.sparkContext.parallelize(
    [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145],
    2
)
num_partitions = numbers_rdd.getNumPartitions()
print("Number of partitions: ", num_partitions)

numbers_GTE_300 = numbers_rdd.filter(lambda x: x >= 300)
retain_peak = numbers_GTE_300.map(lambda x: (x, "PEAK"))

peak_count = retain_peak.count()
print("Peak readings: ", peak_count)

first_3 = retain_peak.take(3)
print("First Three Peaks: ", first_3)

print("The operations that are transformations are .filter() and .map()")
print("The operations that are actions are .count() and .take()")

print("------- Part C -------")
outages = spark.sparkContext.textFile("data/outages.csv")
header = outages.first()
outages_no_header = outages.filter(lambda row: row != header)

parsed_zone_status = outages_no_header.map(lambda row: (
    row.split(",")[2].strip(),
    row.split(",")[6].strip().upper()
    )
)

filtered = parsed_zone_status.filter(lambda x: x[0] != "" and x[1] == "RESOLVED")

zone_counts = (
    filtered.map(lambda x: (x[0], 1))
    .reduceByKey(lambda a, b: a + b)
)

result = zone_counts.sortByKey()

print(result.collect())

print("------- Part C -------")

data = [
    (201, "North", 1480.00),
    (202, "South", 925.50),
    (203, "North", 1710.25),
    (204, "East", 2480.00),
    (205, "South", 1195.75),
    (206, "Central", 3450.50),
    (207, "East", 1890.00),
    (208, "West", 1325.25)
]

columns = [
    "bill_id", "zone", "bill_amount"
]

df = spark.createDataFrame(data, columns)

df.printSchema()

zone_stats = df.groupBy("zone").agg(
    F.count("*").alias("bill_count"),
    F.sum("bill_amount").alias("total_revenue"),
    F.avg("bill_amount").alias("average_bill")
)

zone_stats_rounded = (
    zone_stats
    .withColumn("total_revenue", F.round("total_revenue", 2))
    .withColumn("average_bill", F.round("average_bill", 2))
)

zone_stats_ordered = (
    zone_stats_rounded
    .orderBy(F.col("total_revenue").desc())
)

zone_stats_ordered.explain()
print("Two plan operators seen are: HashAggregate and HashPartitioning")

spark.stop()