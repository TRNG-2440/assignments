from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, avg, round, col
import os

# Setup Spark configurations using class
class SparkClass:
  def __init__(self, appName: str = "Smart Energy Utility Analytics", master: str = "local[*]"):
    self.appName = appName
    self.master = master
  
  # Configurations used to instantiate spark object
  def Configure(self):
   
    # Declare configurations by instantiating spark object
   self.spark = (
   SparkSession.builder 
  .appName(self.appName)
  .master(self.master)
  .getOrCreate()
  )
 
  # Return spark object
  def GetSpark(self) -> SparkSession:
    return self.spark
  
# Instantiate class object
s = SparkClass()

# Execute spark configurations
s.Configure()

# Instantiate spark object
spark = s.GetSpark()

# Streamline sparkContext command
sc = s.GetSpark().sparkContext

# Alert user of any error
sc.setLogLevel("ERROR")

# Display Part A
print(f'\n{20 * '-'} Part A {20 * '-'}\n')

# Display spark version
print(f'Spark version {spark.version}\n')

# Display application name
print(f'Application Name: {sc.appName}\n')

# Display master name
print(f'Master Name: {sc.master}\n')

# Display master name
print(f'Default Paralellism: {sc.defaultParallelism}\n')

# Display master name
print(f'CPU Count: {os.cpu_count()}\n')

# Display Part B
print(f'\n{20 * '-'} Part B {20 * '-'}\n')

# Declare RDD
RDD = sc.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145],2)

# Display # of partitions 
print(f'\nPartitions: {RDD.getNumPartitions()}\n')

# Use filter() to keep readings greater than or equal to 300 units
filterRDD = RDD.filter(lambda l: l >= 300)

# Confirm filtered RDD is operative
print(f'\nFiltered RDD: {filterRDD}\n')

# Display filtered RDD of values equal or greater than 300
print(f'\nFiltered RDD: {filterRDD.collect()}\n')

# Use map() to convert each retained reading of filterRDD into (reading, "PEAK")
mappedRDD = filterRDD.map(lambda l: (l, "PEAK"))

# Confirm mapped RDD is operative
print(f'\nMapped RDD: {mappedRDD}\n')

# Display values of mapped RDD
print(f'\nFiltered RDD: {mappedRDD.collect()}\n')

# Display total count of mapped RDD
print(f'\nMap RDD (Count): {mappedRDD.count()}\n')

# Sorted Mapped RDD in descending order for fun
print(f'\nDisplay the first three peak readings using : {mappedRDD.take(3)}\n')

# Sort RDD
sortedRDD = mappedRDD.sortBy(lambda x: x[0], ascending=False)

# Sorted Mapped RDD in descending order for fun
print(f'\nDisplay sorted mapped values in descending order: {sortedRDD.take(3)}\n')

# Display Part C
print(f'\n{20 * '-'} Part C {20 * '-'}\n')

# Read outages.csv
outagesRDD = sc.textFile("data/outages.csv")

# Print entire outages.csv file
print(outagesRDD.collect(), '\n\n')

# Retrieve header
header = outagesRDD.first()

# Omit header from outagesRDD
outagesRDD = outagesRDD.filter(lambda row: row != header)

# Parse each row and extract zone and status. Trim spaces and convert the status to uppercase.
parsedRDD = outagesRDD.map(
    lambda row: (
        row.split(",")[2].strip(),
        row.split(",")[6].strip().upper()
    )
)

# Remove blank zones and retain only RESOLVED outages
filteredRDD = parsedRDD.filter(lambda row: row[0] != "" and row[1] == "RESOLVED")

# Use map() and reduceByKey() to calculate resolved-outage counts by zone.
countsRDD = (
    filteredRDD
    .map(lambda row: (row[0], 1))
    .reduceByKey(lambda a, b: a + b)
)

# Print countsRDD
print('\n',countsRDD.collect())

# Sort the output alphabetically using sortByKey() and print the results using collect()
sortedCountsRDD = countsRDD.sortByKey()

# Print sortedCountsRDD
print('\nSort by key: ',sortedCountsRDD.collect())

# Sort by value in descending order
countsRDD.sortBy(lambda x: x[1], ascending=False)
print('\nSort by value in descending order: ',sortedCountsRDD.collect())

# Display Part D
print(f'\n{20 * '-'} Part D {20 * '-'}\n')

# Declare list tuple of billing data
billingTuple = [
(201, "North", 1480.00),
(202, "South", 925.50),
(203, "North", 1710.25),
(204, "East", 2480.00),
(205, "South", 1195.75),
(206, "Central", 3450.50),
(207, "East", 1890.00),
(208, "West", 1325.25)
]

# Declare billing dataframe
billingDF = spark.createDataFrame(
  billingTuple,
  ["bill_id", "zone", "bill_amount"]
)

# Display billing dataframe
print(f'Display billing dataframe: {billingDF.collect()}')

print()

# Display billing schema
print("Display billing schema:")
billingDF.printSchema()

# Group by zone and calculate bill count, total revenue and average bill.
metrics = (
    billingDF
    .groupBy("zone")
    .agg(
        count("*").alias("bill_count"),
        round(sum("bill_amount"), 2).alias("total_revenue"),
        round(avg("bill_amount"), 2).alias("average_bill")
    )
    .orderBy(col("total_revenue").desc())
)

# Reveal metrics table
metrics.show()

# Provides execution plan spark will use to execute metrics dataframe.
metrics.explain()

# Stop spark session
spark.stop()

