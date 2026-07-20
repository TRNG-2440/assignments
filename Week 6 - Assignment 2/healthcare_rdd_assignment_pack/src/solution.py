from pyspark.sql import SparkSession
from enum import Enum

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
# Build class that keeps track of RDD validity

class ValidatorClass:
   
   # Paramaterized constructor
   def __init__(self,sc):
    # Declare accumulators - count # of missing values and invalid columns
    self.missingCity = sc.accumulator(0)   
    self.invalidAge = sc.accumulator(0)
    self.invalidBill = sc.accumulator(0)
    self.invalidStatus = sc.accumulator(0)
    self.invalidTotal = sc.accumulator(0)

   # Determine if there are any error or mistakes present in each column
   def Validate(self, v):
    
    # Determine if condition is valid
    isValid = True

    # If value is missing, increment counter and assign false to isValid
    if not v["city"]:
      self.missingCity.add(1); 
      isValid = False

    # If age is 0 or less, increment counter and assign false to isValid
    if v["age"] <= 0:
        self.invalidAge.add(1); 
        isValid = False

    # If bill_amount is 0 or less, increment counter and assign false to isValid
    if v["bill_amount"] <= 0:
        self.invalidBill.add(1); 
        isValid = False

    # If payment_status is not the following: PAID, PENDING or CANCELLED, increment counter and assign false to isValid
    if v["payment_status"] not in {s.value for s in PaymentStatus}:
        self.invalidStatus.add(1); 
        isValid = False

    # Determine if any check failed
    if not isValid:
        self.invalidTotal.add(1)

    return isValid
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
# Perform service charge calculations for Part C
def Service_Charge_Calculations(s, service_charge_map):

  # Calculate service charge percentage of each department
  percentage = service_charge_map.value.get(s["department"],0.0)

  # service_charge = bill_amount * (percentage of service charge)
  s["service_charge"] = round(s["bill_amount"] * percentage, 2)

  # final_amount = bill_amount + service_charge
  s["final_amount"] = round(s["bill_amount"] + s["service_charge"], 2)

  return s
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
  healthCareRDD = healthCareRDD.filter(lambda x: x != header)

  # Print results
  print(healthCareRDD.take(10))

   # Display Part B - Data Validation Using Accumulators
  print(f'\n{20 * '-'} Part B {20 * '-'}\n')

  # Instantiate ValidatorClass object
  vc = ValidatorClass(sc)

   # Parse every row into a dictionary
  healthCareRDD = healthCareRDD.map(ParseRow)

  # Cache the valid parsed RDD
  healthCareRDD = healthCareRDD.filter(vc.Validate).cache()

  # Display valid records
  print("Total data rows:", healthCareRDD.count())

  # Display total missing cities
  print("Total missing cities:", vc.missingCity.value)

  # Display total invalid ages 
  print("Total invalid ages:", vc.invalidAge.value)

  # Display total invalid bills 
  print("Total invalid bills:", vc.invalidBill.value)

  # Display total invalid statuses
  print("Total invalid statuses:", vc.invalidStatus.value)

  # Display # of total invalid rows detected
  print("Total invalid rows:", vc.invalidTotal.value)

  # Display Part C - Broadcast Variable
  print(f'\n{20 * '-'} Part C {20 * '-'}\n')

  # Declare service charge map
  service_charge_map = {
    "Cardiology": 0.18,
    "Orthopedics": 0.12,
    "Dermatology": 0.08,
    "Neurology": 0.15,
    "General Medicine": 0.05,
}
  
  # Broadcast service_charge_map
  service_charge_map = sc.broadcast(service_charge_map)

  # Produce dictionary that contains all the broadcasted charges
  Charges = healthCareRDD.map(lambda x: Service_Charge_Calculations(x, service_charge_map))

  # Print charges
  print(Charges.collect())

  # Display Part D - Transformations to Perform
  print(f'\n{20 * '-'} Part D {20 * '-'}\n')

  # Count # of paid charges using filter tool
  paymentsMade = Charges.filter(lambda c : c["payment_status"] == "PAID")

  # Display # of payments made
  print(f'# of payments paid: {paymentsMade.count()}')

  # Count # of cancelled charges using filter tool
  canceledPayments = Charges.filter(lambda c : c["payment_status"] == "CANCELLED")

  # Display # of canceled payments
  print(f'# of canceled payments: {canceledPayments.count()}')

  # Implement operation to determine distinct cities
  distinctCities = Charges.map(lambda d : d["city"]).distinct()

  # Implement operation to determine distinct department
  distinctDepartments = Charges.map(lambda d : d["department"]).distinct()

  # Display distinct cities 
  print("Distinct cities:", distinctCities.collect())

  # Display distinct departments 
  print("Distinct departments:", distinctDepartments.collect())

  # Determine total city revenue using reduce by key
  totalCityRevenue = (
    paymentsMade
    .map(lambda r: (r["city"], r["final_amount"]))  
    .reduceByKey(lambda x, y: x + y)
)
  # Display total amount of revenue per city
  print("Total amount of revenue per city:", totalCityRevenue.collect())

  # Determine total department revenue using reduce by key
  totalDepartmentRevenue = (
    paymentsMade
    .map(lambda r: (r["department"], r["final_amount"]))
    .reduceByKey(lambda a, b: a + b)
)
  
  # Display total amount of revenue per city
  print("Total amount of revenue per department:", totalDepartmentRevenue.collect())

  # Display Part E - Data Validation Using Accumulators
  print(f'\n{20 * '-'} Part E {20 * '-'}\n')

  # Change name of Charges
  VisitsRDD = Charges

  # Visit per city using countByValue
  print("\nVisits by city:", VisitsRDD.map(lambda r: r["city"]).countByValue())

  # Visits per department using countByValue
  print("\nVisits by dept:", VisitsRDD.map(lambda r: r["department"]).countByValue())
  
  # Total revenue of final amounts using reduce
  totalFinal = VisitsRDD.map(lambda r: r["final_amount"]).reduce(lambda a, b: a + b)

 # Display total revenue of final amounts
  print("\nTotal final_amount : $", totalFinal)

  # Count total # of visits using an accumulator
  visits = sc.accumulator(0)

  # Count total # of visits using foreach
  VisitsRDD.foreach(lambda r: visits.add(1))

  # Print total # of visits using foreach
  print("\nTotal # of visit:", visits.value)  
  
  # Display Part D - Transformations to Perform
  print(f'\n{20 * '-'} Part F {20 * '-'}\n')

  # 1) How many total data rows are available?
  print("\nHow many total data rows are available?:", healthCareRDD.count()) 
  
  # 2) How many valid and invalid records are present?
  print("\nValid:", healthCareRDD.count())             
  print("\nInvalid:", vc.invalidTotal.value)   

  # 3) How many visits happened in each city?
  print(healthCareRDD.map(lambda r: r["city"]).countByValue())

  # 4) How many visits happened in each department?
  print(healthCareRDD.map(lambda r: r["department"]).countByValue())

  # 5) What is the final revenue by city?
  paymentsMade = healthCareRDD.filter(lambda r: r["payment_status"] == "PAID")
  print(
    paymentsMade
    .map(lambda r: (r["city"], r["final_amount"]))
    .reduceByKey(lambda x, y: x + y)
    .collect()
)
  
  # 6) What is the final revenue by department?
  print(
    paymentsMade
    .map(lambda r: (r["department"], r["final_amount"]))
    .reduceByKey(lambda x, y: x + y)
    .collect()
)
  # 7) Which top 3 paid visits generated the highest final amount?
  print(paymentsMade.takeOrdered(3, key=lambda r: -r["final_amount"]))

  # 8) Which departments handled emergency visits?
  print(
    healthCareRDD
    .filter(lambda r: r["visit_type"] == "Emergency")
    .map(lambda r: r["department"])
    .distinct()
    .collect()
)
  # 9) What are all distinct cities and departments?
  print(healthCareRDD.map(lambda r: r["city"]).distinct().collect())

  print(healthCareRDD.map(lambda r: r["department"]).distinct().collect())

  # 10) Which department has the highest average patient rating?
  averageRating = (
    healthCareRDD
    .map(lambda r: (r["department"], (r["rating"], 1)))
    .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
    .mapValues(lambda t: t[0] / t[1])
)
  
  print(averageRating.sortBy(lambda kv: kv[1], ascending=False).first())
 
  # Add newline
  print()





# ---------------------------------------------------------------------
if __name__ == "__main__":
  main()


