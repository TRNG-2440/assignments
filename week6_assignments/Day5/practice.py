from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder.appName("Practice").getOrCreate()


data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data,columns).show()

sc = spark.sparkContext.setLogLevel("ERROR")
rdd =sc.parallelize(data)
rdd.foreach(lambda x: print(x))
spark.stop()
current_dir = Path.cwd().resolve()


