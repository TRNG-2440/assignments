from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as _sum, avg, round as _round
import os

# Part A.

# 1. Create the SparkSession
spark = SparkSession.builder.appName("EnergyUtilityAssignment").master("local[*]").getOrCreate()

# 2. Set the Spark log level to ERROR
spark.sparkContext.setLogLevel("ERROR")

# 3. Print runtime configurations
print(f"Spark Version: {spark.version}")
print(f"Application Name: {spark.sparkContext.appName}")
print(f"Master: {spark.sparkContext.master}")
print(f"Default Parallelism: {spark.sparkContext.defaultParallelism}")
print(f"CPU Count: {os.cpu_count()}") 

# 4. Stop the SparkSession (at the bottom of the screen)

# Part B.

# 1. Create RDD with 2 partitions
data = [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145]
rdd = spark.sparkContext.parallelize(data, 2)

# 2. Print the number of partitions
print(f"Number of partitions: {rdd.getNumPartitions()}")

# 3. Keep readings that are greater than or equal to 300
peaks_rdd = rdd.filter(lambda x: x >= 300)

# 4. Map to (reading, "PEAK")
peak_pairs_rdd = peaks_rdd.map(lambda x: (x, "PEAK"))

# 5. Display peak-reading using count()
print(f"Peak reading count: {peak_pairs_rdd.count()}")

# 6. Display the first three peak readings with take()
print(f"First three peak readings: {peak_pairs_rdd.take(3)}")

#7.
# Transformations create a new RDD and are lazy (don't executed until trigger.)
# #1, #3 and #4 are transformations as filter and map create a new rdd meeting the conditions.
# All other actions are executed upton being triggered

# Part C

# 1. Reads the file
rdd_outages = spark.sparkContext.textFile("outages.csv")

# 2. Dynamically removes the header
header = rdd_outages.first()
rdd_no_header = rdd_outages.filter(lambda row: row != header)

# 3 & 4. Parse, trim, uppercase, and filter blank zones
def process_outage(row):
    cols = row.split(",")
    zone = cols[1].strip()
    status = cols[4].strip().upper() if len(cols) > 4 else ""
    return (zone, status)

processed_rdd = rdd_no_header.map(process_outage).filter(lambda x: x[0] != "" and x[1] == "RESOLVED")

# 5. Sort the output alphabetically using sortByKey() and print the results using collect()
zone_counts = processed_rdd.map(lambda x: (x[0], 1)).reduceByKey(lambda a, b: a + b)

sorted_zone_counts = zone_counts.sortByKey()
print(sorted_zone_counts.collect())

# Part D

# 1. Create DataFrame with original records
billing_data = [
    (201, "North", 1480.00), (202, "South", 925.50), (203, "North", 1710.25),
    (204, "East", 2480.00), (205, "South", 1195.75), (206, "Central", 3450.50),
    (207, "East", 1890.00), (208, "West", 1325.25)
]
columns = ["bill_id", "zone", "bill_amount"]
df_billing = spark.createDataFrame(billing_data, columns)

# Display original records
df_billing.show()

# 2. Print the schema
df_billing.printSchema()

# 3. 
summary_df = df_billing.groupBy("zone").agg(
# 3. Calculate bill count
    count("bill_id").alias("bill_count"),
    
# 4. Calculate total revenue AND round to 2 decimal places
    _round(_sum("bill_amount"), 2).alias("total_revenue"),
    
# 5. Calculate average bill AND round to 2 decimal places
    _round(avg("bill_amount"), 2).alias("average_bill")
).orderBy(col("total_revenue").desc())

# 6. Display report and explain plan
summary_df.show()
summary_df.explain()

# Part 1D
spark.stop()
