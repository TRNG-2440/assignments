from pyspark.sql import SparkSession
from pyspark.sql.functions import count, sum, avg
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def main() -> None:
    # Create a Spark session
    spark = (
        SparkSession.builder
        .appName("Billing Summary")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    # Create a DataFrame from a list 
    billing_data = [
        (201, "North", 1480.00),
        (202, "South", 925.50),
        (203, "North", 1710.25),
        (204, "East", 2480.00),
        (205, "South", 1195.75),
        (206, "Central", 3450.50),
        (207, "East", 1890.00),
        (208, "West", 1325.25)
    ]

    # Create a Spark RDD
    billing_rdd = spark.sparkContext.parallelize(billing_data)
    
    billing_df = billing_rdd.toDF(
        ["bill_id", "zone", "amount"]
    )


    print("=== Original Billing Records ===")
    billing_df.show()


    print("=== Schema ===")
    billing_df.printSchema()


    # GROUP BY + AGGREGATIONS
    billing_summary = billing_df.groupBy("zone").agg(
        count("bill_id").alias("bill_count"),
        sum("amount").alias("total_revenue"),
        avg("amount").alias("average_bill")
    )


    # Round values
    billing_summary = (
        billing_summary
        .withColumn(
            "total_revenue",
            billing_summary["total_revenue"].cast("decimal(10,2)")
        )
        .withColumn(
            "average_bill",
            billing_summary["average_bill"].cast("decimal(10,2)")
        )
    )


    # Sort by total_revenue descending
    billing_summary = billing_summary.sort(
        "total_revenue",
        ascending=False
    )

    print("=== Billing Summary ===")
    billing_summary.show()

    print("=== Execution Plan ===")
    billing_summary.explain()

    print("=== Plan Operators ===")
    print(
        "1. Aggregate: groupBy(zone), count(bill_id), sum(amount), avg(amount)"
    )
    print(
        "2. Sort: order results by total_revenue descending"
    )


    spark.stop()


if __name__ == "__main__":
    main()