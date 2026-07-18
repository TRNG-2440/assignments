from __future__ import annotations

import csv
import os
import shutil
from pathlib import Path
from typing import Any, Dict

os.environ.setdefault(
    "PYSPARK_SUBMIT_ARGS",
    "--conf spark.ui.showConsoleProgress=false pyspark-shell",
)

from pyspark.sql import SparkSession


def prepare_spark_input(source_path: Path) -> str:
    """Copy CSV to a simple Windows-safe Spark input folder."""
    source_path = source_path.resolve()
    if os.name == "nt":
        target_dir = Path("C:/spark_rdd_input")
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / source_path.name
        shutil.copy2(source_path, target_file)
        return target_file.as_posix()
    return source_path.as_posix()


def create_spark() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("HealthcarePatientVisitRDD")
        .master("local[4]")
        .config("spark.driver.host", "127.0.0.1")
        .config("spark.driver.bindAddress", "127.0.0.1")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.local.dir", "C:/spark-temp" if os.name == "nt" else "/tmp/spark-temp")
        .config("spark.sql.warehouse.dir", "C:/spark-warehouse" if os.name == "nt" else "/tmp/spark-warehouse")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark


def parse_line(line: str) -> Dict[str, Any]:
    row = next(csv.reader([line]))
    return {
        "visit_id": row[0].strip(),
        "visit_date": row[1].strip(),
        "patient_id": row[2].strip(),
        "patient_name": row[3].strip(),
        "age": int(row[4]),
        "city": row[5].strip(),
        "department": row[6].strip(),
        "doctor_id": row[7].strip(),
        "visit_type": row[8].strip(),
        "diagnosis": row[9].strip(),
        "bill_amount": float(row[10]),
        "payment_status": row[11].strip().upper(),
        "rating": int(row[12]),
    }


ALLOWED_STATUSES = {"PAID", "PENDING", "CANCELLED"}


def is_valid(record: Dict[str, Any]) -> bool:
    """Pure predicate (no side effects) used for the valid/invalid filter."""
    return (
        bool(record["city"])
        and record["age"] > 0
        and record["bill_amount"] > 0
        and record["payment_status"] in ALLOWED_STATUSES
    )


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    csv_path = project_dir / "healthcare_patient_visits.csv"
    spark_csv_path = prepare_spark_input(csv_path)

    spark = create_spark()
    sc = spark.sparkContext

    # --- Part B: accumulators ---
    missing_city_acc = sc.accumulator(0)
    invalid_age_acc = sc.accumulator(0)
    invalid_bill_acc = sc.accumulator(0)
    invalid_status_acc = sc.accumulator(0)
    invalid_total_acc = sc.accumulator(0)

    def validate_and_accumulate(record: Dict[str, Any]) -> None:
        """Side-effecting validation used only inside foreach() (Part E.8)."""
        is_bad = False
        if not record["city"]:
            missing_city_acc.add(1)
            is_bad = True
        if record["age"] <= 0:
            invalid_age_acc.add(1)
            is_bad = True
        if record["bill_amount"] <= 0:
            invalid_bill_acc.add(1)
            is_bad = True
        if record["payment_status"] not in ALLOWED_STATUSES:
            invalid_status_acc.add(1)
            is_bad = True
        if is_bad:
            invalid_total_acc.add(1)

    # --- Part C: broadcast variable ---
    service_charge_map = {
        "Cardiology": 0.18,
        "Orthopedics": 0.12,
        "Dermatology": 0.08,
        "Neurology": 0.15,
        "General Medicine": 0.05,
    }
    service_charge_bc = sc.broadcast(service_charge_map)

    def enrich(record: Dict[str, Any]) -> Dict[str, Any]:
        pct = service_charge_bc.value.get(record["department"], 0.0)
        service_charge = record["bill_amount"] * pct
        final_amount = record["bill_amount"] + service_charge
        return {
            **record,
            "service_charge_pct": pct,
            "service_charge": round(service_charge, 2),
            "final_amount": round(final_amount, 2),
        }

    try:
        # --- Part A: RDD creation ---
        raw_rdd = sc.textFile(spark_csv_path, minPartitions=4)
        header = raw_rdd.first()

        data_rdd = raw_rdd.filter(lambda line: line != header and bool(line.strip()))
        parsed_rdd = data_rdd.map(parse_line).cache()

        # Part E.8: foreach() action drives the accumulators (side effects only here)
        parsed_rdd.foreach(validate_and_accumulate)

        valid_rdd = parsed_rdd.filter(is_valid).cache()
        enriched_rdd = valid_rdd.map(enrich).cache()
        paid_rdd = enriched_rdd.filter(lambda r: r["payment_status"] == "PAID").cache()

        print("=== Part B: Validation ===")
        print("Total data rows:", data_rdd.count())            # Q1
        print("Valid rows:", valid_rdd.count())                # Q2
        print("Invalid rows (accumulator):", invalid_total_acc.value)
        print("  Missing city:", missing_city_acc.value)
        print("  Invalid age:", invalid_age_acc.value)
        print("  Invalid bill amount:", invalid_bill_acc.value)
        print("  Invalid payment status:", invalid_status_acc.value)

        print("\n=== Preview ===")
        print("First valid record:", enriched_rdd.first())
        print("Take 3 valid records:", enriched_rdd.take(3))    # Part E.3

        print("\n=== Q9: Distinct cities & departments ===")
        print("Cities:", enriched_rdd.map(lambda r: r["city"]).distinct().sortBy(lambda x: x).collect())
        print("Departments:", enriched_rdd.map(lambda r: r["department"]).distinct().sortBy(lambda x: x).collect())

        print("\n=== Q3: Visits per city ===")
        print(enriched_rdd.map(lambda r: r["city"]).countByValue())

        print("\n=== Q4: Visits per department ===")
        print(enriched_rdd.map(lambda r: r["department"]).countByValue())

        print("\n=== Q5: Final revenue by city (paid visits) ===")
        print(
            paid_rdd
            .map(lambda r: (r["city"], r["final_amount"]))
            .reduceByKey(lambda a, b: a + b)
            .mapValues(lambda amt: round(amt, 2))
            .sortBy(lambda pair: pair[1], ascending=False)
            .collect()
        )

        print("\n=== Q6: Final revenue by department (paid visits) ===")
        print(
            paid_rdd
            .map(lambda r: (r["department"], r["final_amount"]))
            .reduceByKey(lambda a, b: a + b)
            .mapValues(lambda amt: round(amt, 2))
            .sortBy(lambda pair: pair[1], ascending=False)
            .collect()
        )

        print("\n=== Q7: Top 3 paid visits by final amount ===")
        print(paid_rdd.takeOrdered(3, key=lambda r: -r["final_amount"]))

        print("\n=== Total paid revenue (reduce) ===")
        total_paid_revenue = paid_rdd.map(lambda r: r["final_amount"]).reduce(lambda a, b: a + b)
        print(round(total_paid_revenue, 2))                     # Part E.6

        print("\nTags using flatMap:")
        print(
            enriched_rdd
            .flatMap(lambda r: [f"city:{r['city']}", f"dept:{r['department']}", f"type:{r['visit_type']}"])
            .map(lambda tag: (tag, 1))
            .reduceByKey(lambda a, b: a + b)
            .sortByKey()
            .collect()
        )

        print("\nVisit IDs grouped by department:")
        print(
            enriched_rdd
            .map(lambda r: (r["department"], r["visit_id"]))
            .groupByKey()
            .mapValues(lambda ids: sorted(list(ids)))
            .sortByKey()
            .collect()
        )

        print("\n=== Q8: Departments that handled Emergency visits ===")
        print(
            enriched_rdd
            .filter(lambda r: r["visit_type"] == "Emergency")
            .map(lambda r: r["department"])
            .distinct()
            .sortBy(lambda x: x)
            .collect()
        )

        opd_patients = enriched_rdd.filter(lambda r: r["visit_type"] == "OPD").map(lambda r: r["patient_id"])
        emergency_patients = enriched_rdd.filter(lambda r: r["visit_type"] == "Emergency").map(lambda r: r["patient_id"])
        print("\nUnique OPD or Emergency patient IDs using union:")
        print(opd_patients.union(emergency_patients).distinct().sortBy(lambda x: x).collect())

        print("\n=== Q10: Department with highest average rating ===")
        dept_avg_rating_rdd = (
            enriched_rdd
            .map(lambda r: (r["department"], (r["rating"], 1)))
            .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
            .mapValues(lambda v: round(v[0] / v[1], 2))
        )
        print("All department averages:", dept_avg_rating_rdd.sortBy(lambda pair: pair[1], ascending=False).collect())
        top_rated_dept = dept_avg_rating_rdd.reduce(lambda a, b: a if a[1] >= b[1] else b)
        print("Highest average rating:", top_rated_dept)

        print("\nPartition demo:")
        print("Original:", enriched_rdd.getNumPartitions())
        print("Repartitioned:", enriched_rdd.repartition(6).getNumPartitions())
        print("Coalesced:", enriched_rdd.repartition(6).coalesce(2).getNumPartitions())

    finally:
        service_charge_bc.unpersist()
        spark.stop()


if __name__ == "__main__":
    main()
