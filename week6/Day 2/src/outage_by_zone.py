from pyspark.sql import SparkSession  # type: ignore
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIR / "data" / "outages.csv"


def main() -> None:
    # Create a Spark session
    spark = (
        SparkSession.builder
        .appName("RDD Outage Count by Zone")
        .master("local[*]")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")

    # Read CSV using Spark RDD
    outages = spark.sparkContext.textFile(str(FILE_PATH))

    print("Rows loaded:", outages.count())

    # Remove header safely
    header = outages.first()

    outages = outages.filter(lambda row: row != header)

    print("\nAfter removing header:")
    print(outages.take(5))


    # Split each row and extract zone + status
    outages = outages.map(
        lambda row: (
            row.split(",")[2].strip(),
            row.split(",")[6].strip().upper()
        )
    )

    print("\nAfter parsing zone and status:")
    print(outages.take(5))


    # Remove blank zones and keep only resolved outages
    outages = outages.filter(
        lambda x: x[0] != "" and x[1] == "RESOLVED"
    )

    print("\nResolved outages only:")
    print(outages.take(10))


    # Convert to key/value pairs and count by zone
    results = (
        outages
        .map(lambda x: (x[0], 1))
        .reduceByKey(lambda a, b: a + b)
        .sortByKey()
        .collect()
    )

    print("\n=== Outage Count by Zone ===\n")

    if not results:
        print("No resolved outages found.")
    else:
        for zone, count in results:
            print(f"{zone}: {count}")


    spark.stop()


if __name__ == "__main__":
    main()