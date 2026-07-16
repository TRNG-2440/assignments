from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("PeakConsumptionAnalysis")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

numbers = spark.sparkContext.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 2)

print(f"Partitions: {numbers.getNumPartitions()}")

# keep readings greater than or equal to 300 units (transformation)
high_numbers = numbers.filter(lambda number:number >= 300)
# convert each retained reading into (reading, "PEAK") (transformation)
peak_readings = high_numbers.map(lambda reading:(reading, "PEAK"))
# display peak-reading count (action)
print(f"Peak-reading count: {peak_readings.count()}")
# display first 3 peak readings (action)
print(f"First 3 peak readings: {peak_readings.take(3)}")

spark.stop()