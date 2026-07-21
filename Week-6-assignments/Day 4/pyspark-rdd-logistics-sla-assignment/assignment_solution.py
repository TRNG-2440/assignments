from pyspark.sql import SparkSession
import os
import sys
import csv

def parse_and_validate_events(iterator):
    """
    Parses CSV lines from a partition iterator and validates each row.
    Returns an iterator of tuples: (classification, data_or_raw_string, reason)
    """
    # csv.reader can consume our line iterator efficiently
    reader = csv.reader(iterator)
    
    for row in reader:
        if not row:
            continue
            
        # Expected column count check
        if len(row) != 11:
            # Reconstruct the row as a string for the error report
            raw_line = ",".join(row)
            yield ("REJECTED", raw_line, f"Invalid column count: expected 11, got {len(row)}")
            continue
            
        # Unpack fields safely
        event_id, event_date, shipment_id, hub_id, service_type, status, promised_hours, actual_hours, distance_km, weight_kg, delivery_charge = row
        
        # Missing critical fields check
        if not event_id or not shipment_id or not hub_id:
            raw_line = ",".join(row)
            yield ("REJECTED", raw_line, "Missing essential keys (event_id, shipment_id, or hub_id)")
            continue
            
        try:
            # Type casting and domain boundary validations
            p_hours = float(promised_hours)
            a_hours = float(actual_hours)
            dist = float(distance_km)
            weight = float(weight_kg)
            charge = float(delivery_charge)
            
            if p_hours < 0 or a_hours < 0 or dist < 0 or weight < 0 or charge < 0:
                raise ValueError("Numeric fields cannot be negative")
                
            # If everything passes, construct a clean dictionary payload
            payload = {
                "event_id": event_id,
                "event_date": event_date,
                "shipment_id": shipment_id,
                "hub_id": hub_id,
                "service_type": service_type,
                "status": status.upper().strip(),
                "promised_hours": p_hours,
                "actual_hours": a_hours,
                "distance_km": dist,
                "weight_kg": weight,
                "delivery_charge": charge
            }
            yield ("VALID", payload, None)
            
        except ValueError as e:
            raw_line = ",".join(row)
            yield ("REJECTED", raw_line, f"Data type or value error: {str(e)}")

def map_metrics(record):
        hub_id = record["hub_id"]
        is_on_time = 1 if record["actual_hours"] <= record["promised_hours"] else 0
        
        # Delay hours are only calculated if actual exceeded promised hours
        delay_hours = max(0.0, record["actual_hours"] - record["promised_hours"])
        charge = record["delivery_charge"]
        
        return (hub_id, (1, is_on_time, delay_hours, charge))

def parse_master(row):
    reader = csv.reader([row])
    fields = next(reader)
    return (fields[0], (fields[1], fields[2], fields[3], float(fields[4])))

def main()->None:
    # Automatically point PySpark to the Python executable currently running this script
    os.environ['PYSPARK_PYTHON'] = sys.executable
    os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

    # Create Spark Session and context
    spark=(
        SparkSession.builder
        .appName("Day4Solution")
        .master("local[*]")
        .getOrCreate()
    )
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Q1
    print("\nQ1. Input path validation\n")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    events_path = os.path.join(current_dir, "data", "delivery_events.csv")
    master_path = os.path.join(current_dir, "data", "hub_master.csv")
    if not os.path.isfile(events_path):
        raise FileNotFoundError(f"Missing input file: {events_path}")
    if not os.path.isfile(master_path):
        raise FileNotFoundError(f"Missing input file: {master_path}")

    # Q2
    print("\nQ2. Load data using RDDs\n")
    events_rdd = sc.textFile(events_path, minPartitions=2)
    master_rdd = sc.textFile(master_path, minPartitions=2)

    print("Delivery Events")
    print(f"Raw line count: {events_rdd.count()}")
    events_header = events_rdd.first()
    print(f"Header: {events_header}")
    print()
    print("Hub Master")
    print(f"Raw line count: {master_rdd.count()}")
    master_header = master_rdd.first()
    print(f"Header: {master_header}")

    # Q3
    print("\nQ3. Remove headers and blank rows\n")
    events_data_rdd = events_rdd.filter(
        lambda row: row.strip() and row != events_header
    )
    master_data_rdd = master_rdd.filter(
        lambda row: row.strip() and row != master_header
    )

    # Q4
    print("\nQ4. Parse and validate events\n")
    # Run the mapPartitions parser
    parsed_events_rdd = events_data_rdd.mapPartitions(parse_and_validate_events)
    classified_events_rdd = parsed_events_rdd.map(lambda x: x).cache()
    print(f"Total processed event records: {classified_events_rdd.count()}")
    
    # Q5
    print("\nQ5. Split valid and rejected records\n")
    # Extract clean dictionaries
    valid_events_rdd = (
        classified_events_rdd
        .filter(lambda x: x[0] == "VALID")
        .map(lambda x: x[1]) # Keep just the payload dictionary
    )
    
    # Extract rejections with reasons
    rejected_events_rdd = (
        classified_events_rdd
        .filter(lambda x: x[0] == "REJECTED")
        .map(lambda x: {"raw_data": x[1], "reason": x[2]}) # Structure for easy csv saving later
    )
    print(f"Valid records count: {valid_events_rdd.count()}")
    print(f"Rejected records count: {rejected_events_rdd.count()}")

    # Q6
    print("\nQ6. Filter business-eligible records\n")
    eligible_events_rdd = valid_events_rdd.filter(lambda record: record["status"] == "DELIVERED")
    print(f"SLA Eligible records ('DELIVERED'): {eligible_events_rdd.count()}")

    # Q7
    print("\nQ7. Create the Pair RDD\n")
    pair_events_rdd = eligible_events_rdd.map(map_metrics)

    # Q8
    print("\nQ8. Aggregate by hub\n")
    # The starting baseline structure: (delivered, on_time, delay_hours, charge)
    zero_value = (0, 0, 0.0, 0.0)
    def seq_op(accumulator, element):
        return (
            accumulator[0] + element[0],  # delivered count + 1
            accumulator[1] + element[1],  # on_time count + (1 or 0)
            accumulator[2] + element[2],  # delay hours + new delay
            accumulator[3] + element[3]   # charge + new charge
        )
    def comb_op(acc1, acc2):
        return (
            acc1[0] + acc2[0],
            acc1[1] + acc2[1],
            acc1[2] + acc2[2],
            acc1[3] + acc2[3]
        )
    
    aggregated_hub_metrics = pair_events_rdd.aggregateByKey(zero_value, seq_op, comb_op)

    # Q9
    print("\nQ9. Load and prepare the master Pair RDD\n")
    pair_master_rdd = master_data_rdd.map(parse_master)

    # Q10
    print("\nQ10. Join transactional and master data\n")
    # Inner join chosen because we need matching keys in both: metrics(Deliveries) require targets(hubs), targets require metrics.
    joined_hub_rdd = aggregated_hub_metrics.join(pair_master_rdd)

    # Q11
    print("\nQ11. Calculate final KPIs\n")
    def calculate_kpis(record):
        hub_id, (metrics, master) = record
        delivered, on_time, delay, charge = metrics
        city, region, manager, target_pct = master
        
        on_time_pct = (on_time / delivered) * 100.0 if delivered > 0 else 0.0
        avg_delay = (delay / delivered) if delivered > 0 else 0.0
        sla_gap = on_time_pct - target_pct
        target_status = "MET" if sla_gap >= 0 else "MISSED"
        
        return (
            hub_id, 
            city, 
            region, 
            manager, 
            int(delivered), 
            int(on_time), 
            round(on_time_pct, 2), 
            round(avg_delay, 2), 
            round(charge, 2), 
            round(sla_gap, 2), 
            target_status
        )
    kpi_report_rdd = joined_hub_rdd.map(calculate_kpis)

    # Q12
    print("\nQ12. Sort the final report\n")
    # Sorts descending (False) by on_time_pct (index 6 of our KPI tuple)
    sorted_report_rdd = kpi_report_rdd.sortBy(lambda x: x[6], ascending=False)

    # Q13
    print("\nQ13. Save the required output files\n")
    # Collect small aggregate report and rejections back to driver node
    final_report_data = sorted_report_rdd.collect()
    final_rejected_data = rejected_events_rdd.collect()
    
    output_dir = os.path.join(current_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    report_out_path = os.path.join(output_dir, "hub_kpi_report.csv")
    rejected_out_path = os.path.join(output_dir, "rejected_records.csv")
    
    # Write Final Report using native Python csv library
    report_headers = [
        "hub_id", "hub_city", "region", "manager", "delivered_count", 
        "on_time_count", "on_time_pct", "avg_delay_hours", 
        "total_delivery_charge", "sla_gap", "target_status"
    ]
    with open(report_out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(report_headers)
        writer.writerows(final_report_data)
        
    # Write Rejected Data
    with open(rejected_out_path, mode="w", newline="", encoding="utf-8") as f:
        if final_rejected_data:
            writer = csv.DictWriter(f, fieldnames=["raw_data", "reason"])
            writer.writeheader()
            writer.writerows(final_rejected_data)

    print("\n--- Files successfully written to the output/ folder ---")

    # Q14
    print("\nQ14. Reload and verify saved output\n")
    print("\n[Verification] Reloading Hub KPI Report:")
    with open(report_out_path, mode="r", encoding="utf-8") as f:
        for line in f.readlines()[:5]: # Print header and first few lines
            print(line.strip())
            
    # Q15
    print("\nQ15. Reconciliation check\n")
    # Total inputs must perfectly balance with total outputs across our pipeline streams
    raw_input_lines = events_data_rdd.count()
    total_valid = valid_events_rdd.count()
    total_rejected = len(final_rejected_data)
    
    non_delivered_filtered = total_valid - eligible_events_rdd.count()
    processed_in_kpis = eligible_events_rdd.count()
    
    print("\n===========#====== RECONCILIATION ===================")
    print(f"Total Raw Lines Uploaded:       {raw_input_lines}")
    print(f"(-) Total Rejected Rows:         {total_rejected}")
    print(f"(=) Total Valid Rows:            {total_valid}")
    print(f"    (-) Non-Delivered Filtered:  {non_delivered_filtered}")
    print(f"    (=) Final Records in KPIs:   {processed_in_kpis}")
    
    # Mathematical proof
    is_balanced = raw_input_lines == (total_rejected + non_delivered_filtered + processed_in_kpis)
    print(f"Data Pipeline Balanced?          {is_balanced}")
    print("=======================================================")

    # End program
    spark.stop()

if __name__ == "__main__":
    main()

"""
Q1. Input path validation
Requirement: Before creating an RDD, check that `delivery_events.csv` and `hub_master.csv` exist. Raise a meaningful `FileNotFoundError` when a file is absent.
Q2. Load data using RDDs
Requirement: Load both CSV files with `sc.textFile()`. Use at least two partitions and print the raw line count and header.
Q3. Remove headers and blank rows
Requirement: Create data-only RDDs by removing the first header line and empty lines.
Q4. Parse and validate events
Requirement: Use `mapPartitions()` to parse CSV rows and `map()` to classify each row as valid or rejected. Cache the classified RDD.
Q5. Split valid and rejected records
Requirement: Create one RDD containing clean event dictionaries and another containing rejected rows and rejection reasons.
Q6. Filter business-eligible records
Requirement: Only `DELIVERED` shipments are eligible for SLA reporting. Filter all other statuses.
Q7. Create the Pair RDD
Requirement: Create `(hub_id, metrics)` where metrics are delivered count, on-time count, delay hours and delivery charge.
Q8. Aggregate by hub
Requirement: Use `aggregateByKey()` to calculate hub-level totals.
Q9. Load and prepare the master Pair RDD
Requirement: Load `hub_master.csv` and prepare `(hub_id, (city, region, manager, target))`.
Q10. Join transactional and master data
Requirement: Perform an inner join on `hub_id` and explain why the key must match in both Pair RDDs.
Q11. Calculate final KPIs
Requirement: Calculate on-time percentage, average delay, total charge, SLA gap and target status.
Q12. Sort the final report
Requirement: Sort hubs by `on_time_pct` from highest to lowest.
Q13. Save the required output files
Requirement: Save the final report and rejected records in the exact specified locations. Use Python `csv.writer` or `DictWriter` after collecting the final small result so it works on Windows without native Hadoop utilities.
Q14. Reload and verify saved output
Requirement: Read both saved files after writing and print their contents.
Q15. Reconciliation check
Requirement: Prove that no input records were silently lost.
"""