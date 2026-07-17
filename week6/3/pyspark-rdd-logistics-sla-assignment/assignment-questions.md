# PySpark RDD Assignment Questions

**Logistics Delivery SLA Analysis**

## Business Requirement

Build a PySpark RDD pipeline that loads shipment-event and hub-master CSV files, validates rows, separates rejected events, calculates delivery SLA KPIs by hub, joins the result with hub master data, sorts the report, and saves final CSV files.

**Input files:** `data/delivery_events.csv` and `data/hub_master.csv`

**Output files:**

- `output/generated/hub_sla_report/hub_sla_report.csv`
- `output/generated/rejected_delivery_events/rejected_delivery_events.csv`

## Q1. Input path validation

**Requirement:** Before creating an RDD, check that `delivery_events.csv` and `hub_master.csv` exist. Raise a meaningful `FileNotFoundError` when a file is absent.

## Q2. Load data using RDDs

**Requirement:** Load both CSV files with `sc.textFile()`. Use at least two partitions and print the raw line count and header.

## Q3. Remove headers and blank rows

**Requirement:** Create data-only RDDs by removing the first header line and empty lines.

## Q4. Parse and validate events

**Requirement:** Use `mapPartitions()` to parse CSV rows and `map()` to classify each row as valid or rejected. Cache the classified RDD.

## Q5. Split valid and rejected records

**Requirement:** Create one RDD containing clean event dictionaries and another containing rejected rows and rejection reasons.

## Q6. Filter business-eligible records

**Requirement:** Only `DELIVERED` shipments are eligible for SLA reporting. Filter all other statuses.

## Q7. Create the Pair RDD

**Requirement:** Create `(hub_id, metrics)` where metrics are delivered count, on-time count, delay hours and delivery charge.

## Q8. Aggregate by hub

**Requirement:** Use `aggregateByKey()` to calculate hub-level totals.

## Q9. Load and prepare the master Pair RDD

**Requirement:** Load `hub_master.csv` and prepare `(hub_id, (city, region, manager, target))`.

## Q10. Join transactional and master data

**Requirement:** Perform an inner join on `hub_id` and explain why the key must match in both Pair RDDs.

## Q11. Calculate final KPIs

**Requirement:** Calculate on-time percentage, average delay, total charge, SLA gap and target status.

## Q12. Sort the final report

**Requirement:** Sort hubs by `on_time_pct` from highest to lowest.

## Q13. Save the required output files

**Requirement:** Save the final report and rejected records in the exact specified locations. Use Python `csv.writer` or `DictWriter` after collecting the final small result so it works on Windows without native Hadoop utilities.

## Q14. Reload and verify saved output

**Requirement:** Read both saved files after writing and print their contents.

## Q15. Reconciliation check

**Requirement:** Prove that no input records were silently lost.