import os

from pyspark.sql import SparkSession


def main():
    # --------------- Part A ------------------
    spark = (
        SparkSession.builder.appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    print(f"Spark version: {spark.version}")
    print(f"App name: {spark.sparkContext.appName}")
    print(f"Master: {spark.sparkContext.master}")
    print(f"Default parallelism: {spark.sparkContext.defaultParallelism}")
    print(f"CPU count: {os.cpu_count()}")

    spark.stop()


if __name__ == "__main__":
    main()
