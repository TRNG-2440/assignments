import os

from pyspark.sql import SparkSession


def main():
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

    sc = spark.sparkContext
    rdd = sc.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 2)
    print(f"Partition count: {rdd.getNumPartitions()}")
    new_rdd = rdd.filter(lambda x: x > 300).map(lambda x: (x, "PEAK"))
    print(f"Peak-reading count: {new_rdd.count()}")
    print(f"First 3 peak readings: {new_rdd.take(3)}")
    """
    parallelize: Narrow Transformation
    filter: Narrow Transformation
    map: Narrow Transformation
    count: Action
    take: Action
    """
    spark.stop()


if __name__ == "__main__":
    main()
