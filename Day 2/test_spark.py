from pyspark.sql import SparkSession

#PART A
spark = (
    SparkSession.builder
    .appName("EnergyUtilityAssignment")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("Spark Version:", spark.version)
print("Application Name:", spark.sparkContext.appName)
print("Master:", spark.sparkContext.master)
print("CPU Cores:", spark.sparkContext.defaultParallelism)

#PART B
readings = [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]

rdd = spark.sparkContext.parallelize(readings, 2)
print("Number of partitions:", rdd.getNumPartitions())

def greater300(num):
    return num >=300

filtered_readings = rdd.filter(greater300)

label_filtered_readings = filtered_readings.map(lambda reading: reading, "PEAK")

print(f"Number of peak readings: {filtered_readings.count()}")

print(f"First 3 peak readings: {filtered_readings.take(3)}")

#transformations: filter(), map()
#actions: count(), take()



#PART C
outages_rdd = spark.sparkContext.textFile("data/outages.csv")

header = outages_rdd.first()

outages_without_header = outages_rdd.filter(lambda row: row != header)

def zone_status(row):
    column = row.split(",")

    zone = column[2].strip()
    status = column[6].strip().upper()

    return(zone, status)

zone_status_outage = outages_without_header.map(zone_status)

def resolved_outages(row):
    return row[0] != "" and row[1] == "RESOLVED"

filtered_resolved = zone_status_outage.filter(resolved_outages)

zones_map = filtered_resolved.map(lambda row: (row[0], 1))

count_by_zone = zones_map.reduceByKey(lambda x, y: x + y)

sorted_countByZone = count_by_zone.sortByKey()
print(sorted_countByZone.collect())



#PART D
from pyspark.sql import functions as F

billing = [
    (201, "North", 1480.00),
    (202, "South", 925.50),
    (203, "North", 1710.25),
    (204, "East", 2480.00),
    (205, "South", 1195.75),
    (206, "Central", 3450.50),
    (207, "East", 1890.00),
    (208, "West", 1325.25)
]

df = spark.createDataFrame(
    billing,
    ["bill_id", "zone", "bill_amount"]
)

df.show()
df.printSchema()

report = (
    df.groupBy("zone")
        .agg(
            F.count("*").alias("bill_count"),
            F.round(F.sum("bill_amount"), 2).alias("total_revenue"),
            F.round(F.avg("bill_amount"), 2).alias("average_bill")
        )
    .orderBy(F.col("total_revenue").desc())
)

report.show()
report.explain()












spark.stop()