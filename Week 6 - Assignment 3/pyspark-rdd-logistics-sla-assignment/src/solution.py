from pathlib import Path
from pyspark.sql import SparkSession 

# ----------------------------------------------------------------------------------------------------
# Class containing all spark logic
class SparkClass:
   
   # Paramaterized Constructor
   def __init__(self, appName: str = "logistics-sla-assignment", master: str = "local[*]"):
      self.appName = appName
      self.master = master

   # Contains all Spark configurations
   def Configure(self) -> SparkSession:
      self.spark = (
         SparkSession.builder
         .appName(self.appName)
         .master(self.master)
         .getOrCreate()
      )

      return self.spark
      
# ----------------------------------------------------------------------------------------------------

# Declare variable that holds directory of data folder
def ValidatePath(DataDirectory : Path):

  # Check that `delivery_events.csv` and `hub_master.csv` exist. Raise a meaningful `FileNotFoundError` when a file is absent.
  deliveryEventsPath = DataDirectory / "delivery_events.csv"
  
  hubMasterPath = DataDirectory / "hub_master.csv"

  # Determine if delivery_events.csv and or hub_master.csv is missing from directory (.../pyspark-rdd-logistics-sla-assignment/data)
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
        value = line.split(",")
        yield {
            "event_id": value[0],
            "event_date": value[1],
            "shipment_id": value[2],
            "hub_id": value[3],
            "service_type": value[4],
            "status": value[5],
            "promised_hours": float(value[6]),
            "actual_hours": float(value[7]),
            "distance_km": float(value[8]),
            "weight_kg": float(value[9]),
            "delivery_charge": float(value[10]),
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

# Turn delivery in (hub,metrics) pair
def HubMetrics(row):
    
    # Amount of time delivery was supposed to take
    promisedHours = row["promised_hours"]   

    # Amount of time delivery actually took
    actualHours = row["actual_hours"]   

    # Determine if actual hours is less than promised hours
    isOnTime = actualHours <= promisedHours
    
    # If delivery was on time, notate there was no delay
    if isOnTime:
       delayedHours = 0

    else:
       delayedHours = actualHours - promisedHours

   # Declare metrics such as:

   # - quantity of delivery

   # - quantity of times delivery was on time 

   # - delayedHours

   # - deivery cost
   
    metricsTuple = (
        1,                          # Quantity of delivery

        1 if isOnTime else 0,       # Number of times delivery was on time

        delayedHours,               # Hours delayed

        row["delivery_charge"],     # Delivery charge
    )
    return (row["hub_id"], metricsTuple)

# ----------------------------------------------------------------------------------------------------

# Add values of both hub tuples together
def AddMetrics(a, b):
    return (
        a[0] + b[0],    # Quantity of deliveries

        a[1] + b[1],    # Quantity of deliveries made on time

        a[2] + b[2],    # Quantity of delayed hours

        a[3] + b[3]     # Total delivery charge
    )

# ----------------------------------------------------------------------------------------------------

# Load `hub_master.csv` and prepare `(hub_id, (city, region, manager, target))`
def HubMasterPair(line):
    value = line.split(",")
    return (value[0], (value[1], value[2], value[3], float(value[4])))

# ----------------------------------------------------------------------------------------------------
def main():

  #  ----------- Q1. Input path validation ----------- 

  # Display Q1
  print(f'\n{20 * '-'}  Q1. Input path validation  {20 * '-'}\n')

  ValidatePath(Path(__file__).resolve().parent.parent / "data")

  #  ----------- Q2. Load data using RDDs ----------- 

  # Display Q2
  print(f'\n{20 * '-'}  Q2. Load data using RDDs  {20 * '-'}\n')

  # Instantiate spark class object
  s = SparkClass()

  # Instantiate spark object
  spark = s.Configure()

  # Instantiate spark context object
  sc = spark.sparkContext

  # Declare RDD by importing content from data/delivery_events.csv
  deliveryRDD = sc.textFile(str(f'{Path(__file__).resolve().parent.parent / "data"}/delivery_events.csv'), minPartitions=2)

  # Declare RDD by importing content from data/hub_master.csv
  hubMasterRDD = sc.textFile(str(f'{Path(__file__).resolve().parent.parent / "data"}/hub_master.csv'), minPartitions=2)

  # Display deliveryRDD
  print(f' Display delivery RDD: ({deliveryRDD.take(5)}')

  # Newline
  print()

  # Display hubMasterRDD
  print(f' Display hubMaster RDD:  ({hubMasterRDD.take(5)}')

  # Newline
  print()

  #  ----------- Q3. Remove headers and blank rows ----------- 

  # Display Q3
  print(f'\n{20 * '-'}  Q3. Remove headers and blank rows  {20 * '-'}\n')

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

  # Newline
  print()

  # Display hubMasterRDD
  print(f' Display hubMaster RDD after mapping:  ({hubMasterRDD.take(5)}')

  # Newline
  print()

  #  ----------- Q4. Parse and validate events ----------- 
  
  # Display Q4
  print(f'\n{20 * '-'}  QQ4. Parse and validate events  {20 * '-'}\n')

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

  # Display Q5
  print(f'\n{20 * '-'}  Q5. Split valid and rejected records  {20 * '-'}\n')

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
  print("\nValid events sample:", validEventsRDD.take(3))

  # Display first 3 rejected results
  print("\nRejected events sample:", rejectedEventsRDD.take(3))

  # Display # of valid rows
  print("\nValid count:", validEventsRDD.count())

  # Display # of rejected rows
  print("\nRejected count:", rejectedEventsRDD.count()) 

  #  ----------- Q6. Filter business-eligible records ----------- 

  # Display Q6
  print(f'\n{20 * '-'}  Q6. Filter business-eligible records  {20 * '-'}\n')

  # Declare RDD which contains all delivery shipments
  deliveredShipmentsRDD = validEventsRDD.filter(lambda row: row["status"] == "DELIVERED")

  # Print first 3 of deliveredShipmentsRDD
  print("\nDelivered Shipments sample:", deliveredShipmentsRDD.take(3))

 # Determine quantity of deliveredShipmentsRDD
  print("\nDelivered Shipments count:", deliveredShipmentsRDD.count()) 

 #  ------------------- Q7. Create the Pair RDD --------------------

  # Display Q7
  print(f'\n{20 * '-'}  Q7. Create the Pair RDD  {20 * '-'}\n')

  # Perform operation to determine HubMetrics
  hubMetricsPairRDD = deliveredShipmentsRDD.map(HubMetrics)

  # Display hubMetricsPairRDD
  print("Pair RDD sample:", hubMetricsPairRDD.take(5)) 
  
   #  ------------------- Q8. Aggregate by hub --------------------

  # Display Q8
  print(f'\n{20 * '-'}  Q8. Aggregate by hub  {20 * '-'}\n')

  # Add tuple of zeros
  zeroValues = (0,0, 0.0, 0.0)

  # Declare RDD that stores hub-level totals
  hubTotalsRDD = hubMetricsPairRDD.aggregateByKey(
     
    zeroValues,      # Starting value of each hub

    AddMetrics,      # Add a row to the hub total

    AddMetrics,      # Combine totals from partitions
)
  # Display hub level totals
  print("Hub totals:", hubTotalsRDD.take(5))

  #  ----------- Q9. Load and prepare the master Pair RDD ------------

  # Display Q9
  print(f'\n{20 * '-'}  Q9. Load and prepare the master Pair RDD  {20 * '-'}\n')

  PairMasterRDD = hubMasterRDD.map(HubMasterPair)

  # Display pair master RDD
  print("Pair Master RDD:", PairMasterRDD.take(5))

  #  ----------- Q10. Join transactional and master data -------------

  # Display Q10
  print(f'\n{20 * '-'} Q10. Join transactional and master data   {20 * '-'}\n')


if __name__ == "__main__":
  main()

