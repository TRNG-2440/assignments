from pyspark.sql import SparkSession


spark = (
    SparkSession.builder.appName("Parallelize")
    .master("local[*]")
    .config("spark.ui.showConsoleProgress", "true")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")
sc = spark.sparkContext
# Existing RDD
original_rdd = sc.parallelize([1, 2, 3, 4, 5])

# Create a new RDD by multiplying each element by 2
new_rdd = original_rdd.map(lambda x: x * 2)

print(new_rdd.collect())
# Output: [2, 4, 6, 8, 10]

spark.stop()
