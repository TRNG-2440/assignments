      


from pathlib import Path
import sys
from pyspark.sql import SparkSession

def main():
    
    #Q1. input path validation
    path = Path.cwd().resolve()

    deliver_path = path / "delivery_events.csv"
    hub_path = path / "hub_master.csv"
    print(path)
    
    try:
        if not deliver_path.exists():
            raise FileNotFoundError("File 'delivery_events.csv' not found")
        if not hub_path.exists():
            raise FileNotFoundError("File 'hub_master.csv' not found.")
    except FileNotFoundError as e:
        print(e)
        sys.exit()

    #Q2 Requirement: Load both CSV files with `sc.textFile()`.
    # Use at least two partitions and print the raw line count and header.
    spark = (
                SparkSession.builder
                .appName("Day4Assignment")
                .master("local[*]")
                .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    raw_delivery_rdd = sc.textFile(deliver_path.as_posix(),minPartitions = 2)
    raw_hub_rdd = sc.textFile(hub_path.as_posix(), minPartitions = 2)

    delivery_header = raw_delivery_rdd.first()
    hub_header = raw_hub_rdd.first()
    print(f"Delivery Events line count: {raw_delivery_rdd.count()}")
    print(f"Delivery Events header: {delivery_header}")
    print()
    print(f"Hub Master line count: {raw_hub_rdd.count()}")
    print(f"Hub Master header: {hub_header}")

    delivery_rdd = raw_delivery_rdd.filter(
        lambda line: line != delivery_header and line.strip()!="")
    hub_rdd = raw_hub_rdd.filter(
        lambda line: line != hub_header and line.strip()!="")




if __name__ == "__main__":
    main()
