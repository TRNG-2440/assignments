from pathlib import Path
from pyspark.sql import SparkSession 

# ----------------------------------------------------------------------------------------------------

# Declare variable that holds directory of data folder
def ValidatePath(DataDirectory : Path):

  # Check that `delivery_events.csv` and `hub_master.csv` exist. Raise a meaningful `FileNotFoundError` when a file is absent.
  deliveryEventsPath = DataDirectory / "delivery_events.csv"
  
  hubMasterPath = DataDirectory / "hub_master.csv"

  # Determine if delivery_events.csv and or hub_master.csv is missing from directory (.../pyspark-rdd-logistics-sla-assignment/data)

  # isMissing = [str(p) for p in (delivery_events_path, hub_master_path) if not p.is_file()]

  missingPaths = []
  for path in (deliveryEventsPath, hubMasterPath):
    if not path.is_file():
        missingPaths.append(str(path))

  # If there are missing paths than throw FileNotFoundError exception
  if missingPaths:
    raise FileNotFoundError(f"Required input file(s) not found: {', '.join(missingPaths)}")

# ----------------------------------------------------------------------------------------------------
# Turn raw CSV text into a dictionary
def ParsePartition(lines):
    for line in lines:
        parts = line.split(",")
        yield {
            "event_id": parts[0],
            "event_date": parts[1],
            "shipment_id": parts[2],
            "hub_id": parts[3],
            "service_type": parts[4],
            "status": parts[5],
            "promised_hours": float(parts[6]),
            "actual_hours": float(parts[7]),
            "distance_km": float(parts[8]),
            "weight_kg": float(parts[9]),
            "delivery_charge": float(parts[10]),
        }

# ----------------------------------------------------------------------------------------------------
# Check validity of dictionary produced by ParsePartition(lines)
def Classify(row):
    if row["hub_id"] == "":
        return ("rejected", row, "Missing hub_id")
    if row["actual_hours"] < 0:
        return ("rejected", row, "Negative actual_hours")
    if row["delivery_charge"] < 0:
        return ("rejected", row, "Negative delivery_charge")
    return ("valid", row, None)

# ----------------------------------------------------------------------------------------------------
def main():

  #  ----------- Q1. Input path validation ----------- 
  ValidatePath(Path(__file__).resolve().parent.parent / "data")

  #  ----------- Q2. Load data using RDDs ----------- 

  # Instantiate spark object
  spark = (SparkSession.builder.appName("logistics-sla-assignment").master("local[*]").getOrCreate())

  # Instantiate spark context object
  sc = spark.sparkContext

  # Declare RDD by importing content from data/delivery_events.csv
  deliveryRDD = sc.textFile(str(f'{Path(__file__).resolve().parent.parent / "data"}/delivery_events.csv'), minPartitions=2)

  # Declare RDD by importing content from data/hub_master.csv
  hubMasterRDD = sc.textFile(str(f'{Path(__file__).resolve().parent.parent / "data"}/hub_master.csv'), minPartitions=2)

  # Display deliveryRDD
  print(f' Display delivery RDD: ({deliveryRDD.take(5)}')

  print()

  # Display hubMasterRDD
  print(f' Display hubMaster RDD:  ({hubMasterRDD.take(5)}')

  print()

  #  ----------- Q3. Remove headers and blank rows ----------- 

  # Declare header for deliveryRDD
  deiveryHeader = deliveryRDD.first()

  # Declare header for hubMasterRDD
  hubMasterHeader = hubMasterRDD.first()

  # Perform operation to remove header and blank rows from deiveryHeader
  deliveryRDD =  deliveryRDD.filter(lambda row: row != deiveryHeader and row.strip() != "")

   # Perform operation to remove header and blank rows from hubMasterHeader 
  hubMasterRDD = hubMasterRDD.filter(lambda row: row != hubMasterHeader and row.strip() != "")

   # Display deliveryRDD
  print(f' Display delivery RDD after mapping: ({deliveryRDD.take(5)}')

  print()

  # Display hubMasterRDD
  print(f' Display hubMaster RDD after mapping:  ({hubMasterRDD.take(5)}')

  print()

  #  ----------- Q4. Parse and validate events ----------- 
  
  # Parse rows into dictionary
  ParsedRDD = deliveryRDD.mapPartitions(ParsePartition)
  
  # Determine if each rows is valid or rejected and cache result
  ClassifiedRDD = ParsedRDD.map(Classify).cache()

  # Display first 5 rows of ClassifiedRDD
  print(ClassifiedRDD.take(5))

  # Display # of valid results
  print("\nValid:", ClassifiedRDD.filter(lambda x: x[0] == "valid").count())

  # Display # of rejected results
  print("\bRejected:", ClassifiedRDD.filter(lambda x: x[0] == "rejected").count())

  #  ----------- Q5. Split valid and rejected records ----------- 

  # RDD of clean event dictionaries
  validEventsRDD = ClassifiedRDD.filter(lambda x: x[0] == "valid").map(lambda x: x[1])

  # RDD of rejected rows + rejection reasons
  rejectedEventsRDD = ClassifiedRDD.filter(lambda x: x[0] == "rejected").map(
    lambda x: {
        **x[1],
        "rejection_reason": x[2],
    }
)
  
  # Display first 3 valid results
  print("Valid events sample:", validEventsRDD.take(3))

  # Display first 3 rejected results
  print("Rejected events sample:", rejectedEventsRDD.take(3))

  # Display # of valid rows
  print("Valid count:", validEventsRDD.count())

  # Display # of rejected rows
  print("Rejected count:", rejectedEventsRDD.count()) 


  


 

 









  

if __name__ == "__main__":
  main()

