from pyspark.sql import SparkSession
import os

spark = (
    SparkSession.builder
    .appName("EnergyUtilityAssignment")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print(f"Version: {spark.version}")
print(f"App Name: {spark.sparkContext.appName}")
print(f"Master: {spark.sparkContext.master}")
print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
print(f"CPU count: {os.cpu_count()}")

spark.stop()