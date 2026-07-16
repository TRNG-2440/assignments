from pyspark import SQLContext, SparkContext, RDD
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
import os

def create_spark() -> SparkSession:
    spark: SparkSession = (
        SparkSession.builder.appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def part_a() -> None:
    spark: SparkSession = create_spark()

    print("Spark Session created Successfully")
    print("Spark Version: ", spark.version)
    print("Application Name : ", spark.sparkContext.appName)
    print("master : ", spark.sparkContext.master)
    print("Default parallelism : ", spark.sparkContext.defaultParallelism)
    print("Cpu count :", os.cpu_count())
    spark.stop()

def part_b(spark: SparkSession) -> None:
    numbers: RDD[int] = spark.sparkContext.parallelize([95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145],
                                             2)
    #Transformation
    readings: RDD[int] = numbers.filter(lambda number: number > 300)
    #Transformation
    peak_readings: RDD[tuple[int, str]] = readings.map(lambda reading: (reading, "PEAK"))
    #Action
    print("Count of peak readings:", peak_readings.count())
    #Action
    print("First 3 peak readings:", peak_readings.take(3))

def part_c(spark: SparkSession) -> None:
    outages: RDD[str] = spark.sparkContext.textFile("data/outages.csv", 2)
    header: str  = outages.first()
    headers: dict[str, int] = {name: i for i, name in enumerate(header.split(","))}
    outages = outages.filter(lambda line: line != header)
    status_zones: RDD[dict[str, str]] = (outages.map(lambda line: {name: line.split(",")[i] for name, i in headers.items()})
                                                .map(lambda row: {"zone": row["zone"].strip(), "status": row["status"].upper().strip()}))

    status_zones = status_zones.filter(lambda row: row["status"] == "RESOLVED" and row["zone"] != "")

    counts_by_zone: RDD[tuple[str, int]] = (status_zones.map(lambda row: (row["zone"], 1))
                      .reduceByKey(lambda left, right: left + right).sortByKey())

    print("Counts by zone:", counts_by_zone.collect())

def part_d(spark: SparkSession) -> None:

    data: list[tuple[int, str, float]] = [
        (201, "North", 1480.00),
        (202, "South", 925.50),
        (203, "North", 1710.25),
        (204, "East", 2480.00),
        (205, "South", 1195.75),
        (206, "Central", 3450.50),
        (207, "East", 1890.00),
        (208, "West", 1325.25),
    ]
    
    data_df: DataFrame = spark.createDataFrame(data, ["bill_id", "zone", "bill_amount"])
    
    print("Schema:", data_df.schema)
    #Group by zone and calculate bill count, total revenue and average bill.
    grouped_df: DataFrame = data_df.groupBy("zone").agg(
        F.count("bill_id").alias("bill_count"),
        F.round(F.sum("bill_amount"), 2).alias("total_revenue"),
        F.round(F.avg("bill_amount"), 2).alias("average_bill")
    )

    grouped_df = grouped_df.sort(grouped_df["total_revenue"].desc())

    grouped_df.show()
    grouped_df.explain()


if __name__ == "__main__":
    part_a()
    spark: SparkSession = create_spark()
    try:
        part_b(spark)
        part_c(spark)
        part_d(spark)
    except Exception as e:
        print(e)
        exit(1)
    finally:
        spark.stop()
