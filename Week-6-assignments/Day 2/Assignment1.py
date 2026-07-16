from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, avg, round
import os
import sys

def main()->None:
    # Automatically point PySpark to the Python executable currently running this script
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
    ##########
    # PART A #
    ##########
    spark=(
        SparkSession.builder
        .appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    #Print Spark version, application name, master, default parallelism and CPU count
    print("\nPart A\n")
    spark_version = spark.version
    app_name = sc.appName
    master = sc.master
    default_par = sc.defaultParallelism
    cpu_count = os.cpu_count()
    print(f"Spark Version:        {spark_version}")
    print(f"Application Name:     {app_name}")
    print(f"Master URL:           {master}")
    print(f"Default Parallelism:  {default_par}")
    print(f"System CPU Count:     {cpu_count}")
    ##########
    # PART B #
    ##########
    print("\nPart B\n")
    rdd_from_list = sc.parallelize(
        [95, 240, 180, 410, 525, 160, 305, 275, 80, 620, 390, 145], 3
    )

    filtered_rdd = rdd_from_list.filter(lambda num: num > 300)
    mapped_rdd = filtered_rdd.map(lambda x: (x, "PEAK"))
    peak_count = mapped_rdd.count()

    print(f"Peak-reading count: {peak_count}")

    first_three_peaks = mapped_rdd.take(3)
    print(f"First three peak readings: {first_three_peaks}")

    ##########
    # PART C
    ##########
    print("\nPart C\n")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "data", "outages.csv")
    raw_rdd = sc.textFile(file_path)

    # Dynamically extract the first row (header)
    header = raw_rdd.first()
    # Filter out the header row to keep only the data rows
    data_rdd = raw_rdd.filter(lambda row: row != header)

    # Parse and filter
    parsed_rdd = data_rdd \
    .map(lambda row: row.split(",")) \
    .map(lambda cols: (cols[2].strip(), cols[6].strip().upper())) \
    .filter(lambda pair: pair[0] != "" and pair[1] == "RESOLVED")
    
    # Calculate resolved outages by zone
    resolved_counts = parsed_rdd \
    .map(lambda pair: (pair[0], 1)) \
    .reduceByKey(lambda a, b: a + b)

    # Sort
    sorted_results = resolved_counts.sortByKey(ascending=True)

    # Print Results
    for zone, zone_count in sorted_results.collect():
        print(f"Zone: {zone:<15} | Resolved Outages: {zone_count}")
    
    ##########
    # PART D #
    ##########
    print("\nPart D\n")
    
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
    columns = ["bill_id", "zone", "bill_amount"]

    # Create DataFrame
    df = spark.createDataFrame(data, schema=columns)
    print("Original Billing Records:")
    df.show()

    # Print Schema
    print("DataFrame Schema:")
    df.printSchema()

    # Group by zone and calculate bill count, total revenue and average bill
    # Round monetary values to two decimal places
    summary_df = df.groupBy("zone") \
        .agg(
            count("bill_id").alias("bill_count"),
            round(spark_sum("bill_amount"), 2).alias("total_revenue"),
            round(avg("bill_amount"), 2).alias("avg_bill")
        ) \
        .orderBy(col("total_revenue").desc()) # Order the report by total revenue descending

    # Display the report and call explain(). Identify two plan operators
    print("Billing Summary Report (Sorted by Total Revenue Descending):")
    summary_df.show()
    print("Execution Plan Explanation:")
    summary_df.explain()

    # End program
    spark.stop()


if __name__=="__main__":
    main()
    