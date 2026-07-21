# NOTE: the Purpose of this file is to provide me a basic template I can follow for pyspark assignments to get set up fast
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum as spark_sum, avg, round
import os
import sys

def main()->None:
    # Automatically point PySpark to the Python executable currently running this script
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    # Create Spark Session and context
    spark=(
        SparkSession.builder
        .appName("01_Hospital_Medallion_Pipeline")
        .master("local[*]")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Grabbing a local csv file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "parentFolder", "fileName.csv")
    raw_rdd = sc.textFile(file_path)

    # Dynamically extract the first row (header)
    header = raw_rdd.first()
    # Filter out the header row to keep only the data rows
    data_rdd = raw_rdd.filter(lambda row: row != header)

    # End program
    spark.stop()