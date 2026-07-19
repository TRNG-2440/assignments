from pyspark.sql import SparkSession
from enum import Enum
from pyspark.sql.functions import count, sum, avg, round, col

# Payment status enum
class PaymentStatus(Enum):
    PAID = "PAID"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"

# ---------------------------------------------------------------------

# Build class containing Spark configuration
class SparkClass:

  # Paramaterized constructor
  def __init__(self, appName: str = "Healthcare Patient Visit Analytics", master: str = "local[*]"):
    self.appName = appName
    self.master = master

  # Spark configurations
  def Configure(self):

    # Declare configurations by instantiating spark object
    self.spark = (
      SparkSession.builder
      .appName(self.appName)
      .master(self.master)
      .getOrCreate()
    )
  
  # Return spark object
  def GetSpark(self) -> SparkSession:
    return self.spark

# ---------------------------------------------------------------------
# Parse every row into a dictionary
def ParseRow(row: str) -> dict:

  # Tokenize row into list
  row = row.split(",")

  # Declare list of each column name
  columns = [
    "visit_id", "visit_date", "patient_id", "patient_name", "age", "city",
    "department", "doctor_id", "visit_type", "diagnosis", "bill_amount",
    "payment_status", "rating",
]

  # Pair columns with rows
  dictionary = dict(zip(columns, row))

  # Perform static cast and tokenization on each individual value 
  dictionary["age"] = int(dictionary["age"])
  dictionary["bill_amount"] = float(dictionary["bill_amount"])
  dictionary["rating"] = int(dictionary["rating"])
  dictionary["payment_status"] = dictionary["payment_status"].strip().upper()
  dictionary["city"] = dictionary["city"].strip()

  return dictionary

# ---------------------------------------------------------------------

# Determine if there are any error or mistakes present in each column
def Validate(r):
    
    # Instantiate class object
    s = SparkClass()

    # Execute spark configurations
    s.Configure()

    # Instantiate spark object
    spark = s.GetSpark()

    # Instantiate spark context object
    sc = spark.sparkContext

    # Declare accumulators - count # of missing values and invalid columns
    missingCity = sc.accumulator(0)   
    invalidAge = sc.accumulator(0)
    invalidBill = sc.accumulator(0)
    invalidStatus = sc.accumulator(0)
    invalidTotal = sc.accumulator(0)
    
    # Determine if condition is valid
    isValid = True

    # If value is missing, increment counter and assign false to isValid
    if not r["city"]:
        missingCity.add(1); 
        isValid = False

    # If age is 0 or less, increment counter and assign false to isValid
    if r["age"] <= 0:
        invalidAge.add(1); 
        isValid = False

    # If bill_amount is 0 or less, increment counter and assign false to isValid
    if r["bill_amount"] <= 0:
        invalidBill.add(1); 
        isValid = False

    # If payment_status is not the following: PAID, PENDING or CANCELLED, increment counter and assign false to isValid
    if r["payment_status"] not in {s.value for s in PaymentStatus}:
        invalidStatus.add(1); 
        isValid = False

    # Determine if any check failed
    if not isValid:
        invalidTotal.add(1)

    return isValid

# ---------------------------------------------------------------------

# Main function
def main():

  # Instantiate class object
  s = SparkClass()

  # Execute spark configurations
  s.Configure()

  # Instantiate spark object 
  spark = s.GetSpark()

  # Instantiate spark context object
  sc = spark.sparkContext

  # Detect potential warnings
  sc.setLogLevel("WARN")

  # Display Part A - RDD Creation
  print(f'\n{20 * '-'} Part A {20 * '-'}\n')

  # Declare RDD by importing from "data/healthcare_patient_visits.csv"
  healthCareRDD = sc.textFile("data/healthcare_patient_visits.csv")

  # Declare copy of origin healthCareRdd containing raw data
  RawRDD = healthCareRDD

  # Declare header
  header = healthCareRDD.first()

  # Remove header
  healthCareRdd = healthCareRDD.filter(lambda x: x != header)

  # Parse every row into a dictionary
  healthCareRdd = healthCareRdd.map(ParseRow)

  # Cache the valid parsed RDD
  ealthCareRdd = healthCareRdd.filter(Validate).cache()

# ---------------------------------------------------------------------
if __name__ == "__main__":
  main()
