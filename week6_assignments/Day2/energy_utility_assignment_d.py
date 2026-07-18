import findspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from typing import Iterator
import csv

findspark.init()



def main():
    """Create the DataFrame and display the original records. (4)
    Print the schema. (2)
    Group by zone and calculate bill count, total revenue and average bill. (8)
    Round monetary values to two decimal places. (3)
    Order the report by total revenue descending. (3)
    Display the report and call explain(). Identify two plan operators. (5)"""

    spark = (
                SparkSession.builder
                .appName("EnergyUtilityPartD")
                .master("local[*]")
                .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    billing = [
        (201, "North", 1480.00),
        (202, "South", 925.50),
        (203, "North", 1710.25),
        (204, "East", 2480.00),
        (205, "South", 1195.75),
        (206, "Central", 3450.50),
        (207, "East", 1890.00),
        (208, "West", 1325.25),
    ]

    #bill_id	zone	bill_amount

    billing_df = spark.createDataFrame(
        billing,
        ["bill_id", "zone", "bill_amount"]
        )

    print("Original Data")
    billing_df.show()

    print("Schema")
    billing_df.printSchema()

    billing_report = (
        billing_df
        .groupBy("zone")
        .agg(
            F.count("*").alias("bill_count"),
            F.round(F.sum("bill_amount"), 2).alias("total_revenue"),
            F.round(F.avg("bill_amount"), 2).alias("average_bill"),
            )
        .orderBy(F.desc("total_revenue"))
        )

    print("Report")
    billing_report.show()

    # explain() shows the physical plan. Two operators to look for:
    # - HashAggregate (performs the groupBy/agg count-sum-avg in two stages)
    # - Sort / Exchange (the orderBy triggers a shuffle + sort by total_revenue)
    billing_report.explain()

    spark.stop()

if __name__ == "__main__":
    main()
