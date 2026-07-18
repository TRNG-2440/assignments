import findspark

from pyspark.sql import SparkSession
from pathlib import Path
from typing import Iterator
import csv
import os
findspark.init()



def main():
    """Read outages.csv using spark.sparkContext.textFile(). Remove the header dynamically. (4)
    Parse each row and extract zone and status. Trim spaces and convert the status to uppercase. (4)
    Remove blank zones and retain only RESOLVED outages. (3)
    Use map() and reduceByKey() to calculate resolved-outage counts by zone. (5)
    Sort the output alphabetically using sortByKey() and print the results using collect(). (4)"""

    path = Path.cwd().resolve()
    csv_path = path / "data" / "outages.csv"

    spark_temp = path / ".spark-temp"
    spark_warehouse = path / ".spark-warehouse"

    spark_temp.mkdir(exist_ok=True)
    spark_warehouse.mkdir(exist_ok=True)

    if not csv_path.is_file():
        raise FileNotFoundError(
            "Python cannot find the CSV file:"
        )
    
    spark = (
                SparkSession.builder
                .appName("RetailOrdersRDDStepByStep")
                .master("local[*]")
                .config("spark.driver.host", "127.0.0.1")
                .config("spark.driver.bindAddress", "127.0.0.1")
                .config("spark.ui.showConsoleProgress", "false")
                .config("spark.local.dir", str(spark_temp))
                .config("spark.sql.warehouse.dir", str(spark_warehouse))
                .getOrCreate()  
    )
     

    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    raw_lines_rdd = sc.textFile(
        str(csv_path),
        minPartitions=4,
    ).setName("RawOutagesLines")

    clean_lines_rdd = raw_lines_rdd.mapPartitionsWithIndex(remove_header)
    parsed_rdd = clean_lines_rdd.map(parse_rows)

    resolved_rdd = parsed_rdd.filter(
        lambda row: row["zone"] != "" and row["status"] == "RESOLVED"
    )

    zone_counts_rdd = (
        resolved_rdd.map(lambda row: (row["zone"], 1))
        .reduceByKey(lambda a, b: a + b)
        .sortByKey()
    )

    for zone, count in zone_counts_rdd.collect():
        print(f"{zone}: {count}")

def remove_header(partition_index, iterator):
    if partition_index == 0:
        next(iterator, None)

    yield from iterator #looping under the hood and returning all the rest of the lines

def parse_rows(line):
    cols = next(csv.reader([line]))
    return {
        "zone": cols[2].strip(),
        "status": cols[6].strip().upper(),
    }


if __name__ == "__main__":
    main()