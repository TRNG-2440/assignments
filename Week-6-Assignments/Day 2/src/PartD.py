from pyspark.sql import SparkSession
from pyspark.sql import functions

spark = (
    SparkSession.builder
    .appName("BillingSummary")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

data = [
    (201, "North", 1480.00),
    (202, "South", 925.50),
    (203, "North", 1710.25),
    (204, "East", 2480.00),
    (205, "South", 1195.75),
    (206, "Central", 3450.50),
    (207, "East", 1890.00),
    (208, "West", 1325.25)
]

# create DF and display
bill_df = spark.createDataFrame(data, ["bill_id", "zone", "bill_amount"])
print("Original records: ")
bill_df.show()

# print schema
print("Schema: ")
bill_df.printSchema()

# group by zone and calculate bill count, total revenue, and average bill
bill_df_zone = (bill_df.groupBy("zone")
                .agg(
                    functions.count("*").alias("bill_count"),
                    functions.round(functions.sum("bill_amount"),2).alias("total_revenue"),
                    functions.round(functions.avg("bill_amount"),2).alias("average_bill")
                )
                .orderBy(functions.desc("total_revenue"))
                )

# display
bill_df_zone.show()

# explain
bill_df_zone.explain()
# plan operators: HashAggregate, Sort

spark.stop()