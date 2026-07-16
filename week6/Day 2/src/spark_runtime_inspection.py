import os
import sys
from pyspark.sql import SparkSession


os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
def main() -> None:
    # Create a Spark session
    spark = (
        SparkSession.builder
        .appName("Energy Utility Assignment")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    print("Spark session created successfully.")
    print("Spark version:", spark.version)
    print("Application name: ", spark.sparkContext.appName)
    print("Master: ", spark.sparkContext.master)
    print("Default parallelism: ", spark.sparkContext.defaultParallelism)
    print("CPU count: ", os.cpu_count())

    spark.stop()


if __name__ == "__main__":
    main()