from pyspark.sql import SparkSession
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
def main()-> None:
    # Create a Spark session
    spark = (
        SparkSession.builder
        .appName("Peak Consumption Analysis")
        .master("local[*]")
        .getOrCreate()
    )
    # Set the Spark log level to ERROR
    spark.sparkContext.setLogLevel("ERROR")

    # Create an RDD from a list of numbers
    numbers = spark.sparkContext.parallelize(
        [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 2
    )

    # Perform peak consumption analysis
    filtered = numbers.filter(lambda x: x >= 300)
    mapped = filtered.map(lambda x: (x, "PEAK"))
    count = mapped.count()
    first_three = mapped.take(3)

    print(f"Number of partitions: {numbers.getNumPartitions()}")
    print(f"Peak-reading count: {count}")
    print(f"First three peak readings: {first_three}")
    
    spark.stop()

if __name__ == "__main__":
    main()