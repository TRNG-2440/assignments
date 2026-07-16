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
        .appName("EnergyUtilityAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # End program
    spark.stop()