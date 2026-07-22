import csv

from pathlib import Path

from pyspark.sql import SparkSession 

# ----------------------------------------------------------------------------------------------------
# Class containing all spark logic
class SparkClass:
   
   # Parameterized Constructor
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

  # Check that `delivery_events.csv` and `hub_master.csv` in designated directories
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

# -------------------------------------------------------------------------------

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

# -------------------------------------------------------------------------------

# Add values of both hub tuples together
def AddMetrics(a, b):
    return (
        a[0] + b[0],    # Quantity of deliveries

        a[1] + b[1],    # Quantity of deliveries made on time

        a[2] + b[2],    # Quantity of delayed hours

        a[3] + b[3]     # Total delivery charge
    )

# -------------------------------------------------------------------------------

# Turn hub master rows into pairs
def HubMasterPair(line):
    value = line.split(",")
    return (value[0], (value[1], value[2], value[3], float(value[4])))

# -------------------------------------------------------------------------------

# Calculate KPI metrics
def CalculateKPIs(row):

    # Determine hub id for each individual row
    hubID = row[0]

    # row[1][0]: (delivered, onTime, delayedHours, totalCharge)
    delivered, onTime, delayedHours, totalCharge = row[1][0]

    # row[1][1]: (city, region, manager, target)
    city, region, manager, target = row[1][1]

    # On-time percentage = (onTime / delivered) * 100
    onTimePercentage = (onTime / delivered) * 100

    # Average delay hours
    averageDelay = delayedHours / delivered

    # how far above/below the SLA target
    sla_gap = onTimePercentage - target

    # If onTimePercentage surpassed target then goal is achieved
    if onTimePercentage >= target:
        targetStatus = "MET"
    else:
        targetStatus = "MISSED"

    return {
        "hub_id": hubID,
        "city": city,
        "region": region,
        "manager": manager,
        "delivered_count": delivered,
        "on_time_count": onTime,
        "on_time_percentage": round(onTimePercentage, 2),
        "avg_delay": round(averageDelay, 2),
        "total_charge": round(totalCharge, 2),
        "sla_target_percentage": target,
        "sla_gap": round(sla_gap, 2),
        "target_status": targetStatus,
    }

# -------------------------------------------------------------------------------

# Write "Hub sla report" and "Rejected delivery events report" to their own file paths
def WriteFile(sortKpiRDD, rejectedEventsRDD):
   directory = Path(__file__).resolve().parent.parent
   
   # Declare hub_sla_report_path and rejected_delivery_events_path
   hub_sla_report_path = directory / "output" / "generated" /"hub_sla_report" / "hub_sla_report.csv"
   rejected_delivery_events_path = directory / "output" / "generated" /"rejected_delivery_events" / "rejected_delivery_events.csv"

   # Create folders for hub_sla_report_path and rejected_delivery_events_path if they currently don't exist
   hub_sla_report_path.parent.mkdir(parents=True, exist_ok=True)
   rejected_delivery_events_path.parent.mkdir(parents=True, exist_ok=True)

   # Convert from RDD to list
   hubReportList = sortKpiRDD.collect()
   rejectedEventsList = rejectedEventsRDD.collect()  

   # Write final SLA report
   with open(hub_sla_report_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(hubReportList[0].keys()))
    writer.writeheader()
    writer.writerows(hubReportList)

    # Write rejected record report
   with open(rejected_delivery_events_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=list(rejectedEventsList[0].keys()))
    writer.writeheader()
    writer.writerows(rejectedEventsList)

    # Confirm results were successfully written
    print("Saved:", hub_sla_report_path)
    print("Saved:", rejected_delivery_events_path)

# -------------------------------------------------------------------------------

# Read both saved files after writing and print their contents
def ReadFile(hub_sla_report_path : Path, rejected_delivery_events_path: Path) -> tuple:

    # Declare variable used to read file contents
    hub_sla_report = ""
    rejected_delivery_events = ""

    # Read hub_sla_report_path.csv and display results
    with open(hub_sla_report_path, newline="") as file:
       hub_sla_report = list(csv.DictReader(file))
    
    # Read rejected_delivery_events.csv and display results
    with open(rejected_delivery_events_path, newline="") as file:
        rejected_delivery_events = list(csv.DictReader(file))

    return (hub_sla_report, rejected_delivery_events)

# -------------------------------------------------------------------------------
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
  print("\nPair RDD sample:", hubMetricsPairRDD.take(5)) 
  
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
  # Display hub totals
  print("\nHub totals:", hubTotalsRDD.take(5))

  #  ----------- Q9. Load and prepare the master Pair RDD ------------

  # Display Q9
  print(f'\n{20 * '-'}  Q9. Load and prepare the master Pair RDD  {20 * '-'}\n')

  PairMasterRDD = hubMasterRDD.map(HubMasterPair)

  # Display pair master RDD
  print("\nPair Master RDD:", PairMasterRDD.take(5))

  #  ----------- Q10. Join transactional and master data -------------

  # Display Q10
  print(f'\n{20 * '-'} Q10. Join transactional and master data {20 * '-'}\n')

  # Execute inner join on hub_id
  joinedRDD = hubTotalsRDD.join(PairMasterRDD)

  print("\nJoined sample:", joinedRDD.take(3))

#  -----------  Q11. Calculate final KPIs -------------

  # Display Q11
  print(f'\n{20 * '-'} Calculate final KPIs {20 * '-'}\n')

  # Calculate KPI metrics
  kpiRDD = joinedRDD.map(CalculateKPIs)

  # Print KPI sample
  print("\nKPI sample:", kpiRDD.take(3))    

#  -----------  Q12. Sort the final report -------------

  # Display Q12
  print(f'\n{20 * '-'} Sort the final report {20 * '-'}\n')

  # Sort hubs by `on_time_pct` from highest to lowest.
  sortKpiRDD = kpiRDD.sortBy(lambda row: row['on_time_percentage'], ascending = False)

  # Display sorted result
  print(f'\nSort hubs by `on_time_pct` from highest to lowest: {sortKpiRDD.collect()}')

#  -----------  Q13. Save the required output files -------------

  # Display Q13
  print(f'\n{20 * '-'} Save the required output files {20 * '-'}\n')

  # Write "Hub sla report" and "Rejected delivery events report" to their own file paths
  WriteFile(sortKpiRDD, rejectedEventsRDD)

#  -----------  Q14. Save the required output files -------------

  # Display Q14
  print(f'\n{20 * '-'} Reload and verify saved output {20 * '-'}\n')

  # Declare root file directory
  directory = Path(__file__).resolve().parent.parent

  # Declare hub_sla_report_path and rejected_delivery_events_path
  hub_sla_report_path = directory / "output" / "generated" / "hub_sla_report" / "hub_sla_report.csv"
  rejected_delivery_events_path = directory / "output" / "generated" / "rejected_delivery_events" / "rejected_delivery_events.csv"

  # Read both saved files after writing and print their contents
  (hub_sla_report, rejected_delivery_events) = ReadFile(hub_sla_report_path, rejected_delivery_events_path)

  # Print hubReport results
  print(f'\n-------- Hub SLA Report --------\n{hub_sla_report}')

  # Print rejectionReport results
  print(f'\n----- Rejected Delivery Events -----\n{rejected_delivery_events}')

  #  -----------  Q15.Reconciliation check -------------

  # Display Q15
  print(f'\n{20 * "-"} Reconciliation check {20 * "-"}\n')

  # Display results of reconciliation check
  print(f"\nDelivery Event row quantity:     {deliveryRDD.count()}")

  print(f"\nValid Event row quantity:        {validEventsRDD.count()}")

  print(f"\nRejected Event row quantity:     {rejectedEventsRDD.count()}")

  print(f"\nValid Events + Rejected Events:  {validEventsRDD.count() + rejectedEventsRDD.count()}")

  # Determine if sum of validEventsRDD rows and rejectedEventsRDD rows equate to total delivery count
  if (validEventsRDD.count() + rejectedEventsRDD.count()) == deliveryRDD.count():
     print(f'\n{40 * "-"}')
     print(f'\nResult: Reconciliation check is valid\n')
    
  else:
     print(f'\n{40 * "-"}')
     print(f'\nResult: Reconciliation check is invalid\n')

  # Terminate spark 
  spark.stop()

if __name__ == "__main__":
  main()

