from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("OutageCount")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

# read outages.csv and remove headers
outages_with_header = spark.sparkContext.textFile("data/outages.csv")
header = outages_with_header.first()
outages = outages_with_header.filter(lambda row:row != header)

# extract zone and status. Trim spaces and convert the status to uppercase
def get_zone_and_status(row):
    row_list = row.split(",")
    zone = row_list[2]
    zone = zone.replace(" ", "") # replacing spaces
    status = row_list[-1]
    status = status.replace(" ", "") # replacing spaces
    status = status.upper() # converting status to uppercase
    return (zone, status)

zone_and_status = outages.map(get_zone_and_status)

# remove blank zones and retain only RESOLVED changes
zone_and_resolved = zone_and_status.filter(lambda zone_status: zone_status[0] and zone_status[1] == "RESOLVED")

# calculate resolved-outage counts by zone
zone_and_resolved_num = zone_and_resolved.map(lambda row: (row[0], 1))
resolved_outage_counts = zone_and_resolved_num.reduceByKey(lambda count1, count2: count1 + count2)

# sort the output alphabetically and print the results
resolved_outage_counts = resolved_outage_counts.sortByKey()
print(f"Resolved outage counts grouped by zone: {resolved_outage_counts.collect()}")

spark.stop()