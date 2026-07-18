import csv
from datetime import date, datetime
import io
import os
from pathlib import Path
import re
import shutil
from typing import Any, Dict, Iterable, List
from pyspark import RDD
from pyspark.sql import SparkSession

# Pre-compiled REGEX Patterns
PATTERN_EVT = re.compile(r"^EVT-\d{4}")
PATTERN_SHP = re.compile(r"^SHP-\d{4}")
PATTERN_HUB = re.compile(r"^HUB-[A-Z]{3}")
PATTERN_ALPHA = re.compile(r"[a-zA-Z]+")


# -------------- Helper functions ----------------
def is_past_date(date_str) -> bool:
    """Helper to check if a date string is formatted correctly and in the past."""
    try:
        parsed_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
        return parsed_date < date.today()
    except ValueError:
        return False


def is_positive_numeric(val, num_type) -> bool:
    try:
        converted = num_type(val)
        return converted > 0
    except ValueError:
        return False


def is_percentage(val) -> bool:
    try:
        converted = float(val)
        return 0.0 <= converted <= 100.0
    except ValueError:
        return False


VALIDATION_CONFIG = {
    "delivery_events.csv": {
        "expected_columns_length": 11,
        "expected_columns": [
            "event_id",
            "event_date",
            "shipment_id",
            "hub_id",
            "service_type",
            "status",
            "promised_hours",
            "actual_hours",
            "distance_km",
            "weight_kg",
            "delivery_charge",
        ],
        "rules": {
            0: lambda x: bool(PATTERN_EVT.match(x.strip())),
            1: lambda x: is_past_date(x),
            2: lambda x: bool(PATTERN_SHP.match(x.strip())),
            3: lambda x: bool(PATTERN_HUB.match(x.strip())),
            4: lambda x: x.strip() in {"EXPRESS", "STANDARD", "SAME_DAY"},
            5: lambda x: (
                x.strip()
                in {"FAILED", "DELIVERED", "RETURNED", "IN_TRANSIT", "UNKNOWN"}
            ),
            6: lambda x: is_positive_numeric(x, int),
            7: lambda x: is_positive_numeric(x, int),
            8: lambda x: is_positive_numeric(x, int),
            9: lambda x: is_positive_numeric(x, float),
            10: lambda x: is_positive_numeric(x, float),
        },
    },
    "hub_master.csv": {
        "expected_columns_length": 5,
        "expected_columns": [
            "hub_id",
            "hub_city",
            "region",
            "manager",
            "sla_target_pct",
        ],
        "rules": {
            0: lambda x: bool(PATTERN_HUB.match(x.strip())),
            1: lambda x: bool(PATTERN_ALPHA.search(x)),
            2: lambda x: x.strip() in {"South", "West", "South-Central"},
            3: lambda x: bool(PATTERN_ALPHA.search(x)),
            4: lambda x: is_percentage(x),
        },
    },
}
ValidationResult = Dict[str, Any]


def check_file_exist(path: Path) -> bool:
    return os.path.exists(path) and os.path.isfile(path)


def check_files_exist(files: List[Path]) -> List[bool]:
    return [check_file_exist(file_path) for file_path in files]


def get_file_paths(file_names: List[str], DATA_DIR: Path) -> List[Path]:
    return [DATA_DIR.joinpath(Path(file_name)) for file_name in file_names]


def load_files(file_paths: List[Path]) -> List[RDD[str]]:
    rdd_list = []
    for file_path in file_paths:
        rdd = sc.textFile(str(file_path), 2)
        print(f"Loaded file: {file_path.name}")
        print(f"Line count: {rdd.count()}")
        print(f"Header: {rdd.first()}\n")
        rdd_list.append(rdd)
    return rdd_list


def parse_csv_partitions(partitions: Iterable[str]) -> Iterable:
    for partition in partitions:
        f = io.StringIO(partition)
        reader = csv.reader(f)
        for row in reader:
            yield row


def validate_line(row: List[str], config: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if len(row) != config["expected_columns_length"]:
            return {
                "is_valid": False,
                "record": None,
                "raw_line": row,
                "errors": [
                    f"Expected {config['expected_columns_length']} columns, but received only {len(row)}"
                ],
            }

        is_valid = True
        errors = []
        for idx, rule in config["rules"].items():
            if not rule(row[idx]):
                is_valid = False
                errors.append(f"Rule failed at column {idx}")

        record = {}
        if is_valid:
            for idx, column in enumerate(config["expected_columns"]):
                record[column] = row[idx]
        return {
            "is_valid": is_valid,
            "record": record,
            "raw_line": row,
            "errors": errors,
        }
    except (ValueError, csv.Error) as e:
        return {
            "is_valid": False,
            "record": None,
            "raw_line": row,
            "errors": [f"Parsing error: {e}"],
        }


def clean_rdds(
    rdd_list: List[RDD[str]], file_names: List[str]
) -> List[RDD[Dict[str, Any]]]:
    cleaned_rdds = []
    for file_name, rdd in zip(file_names, rdd_list):
        print(f"\nParsing and validating {file_name}...")
        header = rdd.first()
        rdd_data = rdd.filter(lambda line, hd=header: line != hd and bool(line.strip()))
        rdd_data_cleaned = rdd_data.mapPartitions(parse_csv_partitions).map(
            lambda x, fn=file_name: validate_line(x, VALIDATION_CONFIG[fn])
        )
        rdd_data_cleaned.cache()
        cleaned_rdds.append(rdd_data_cleaned)
    return cleaned_rdds


def map_to_metrics(record: Dict[str, Any]) -> tuple[Any, tuple[int, int, Any, Any]]:
    hub_id = record["hub_id"]
    promised = int(record["promised_hours"])
    actual = int(record["actual_hours"])
    delivery_charge = float(record["delivery_charge"])

    delivered_cnt = 1
    on_time_cnt = 1 if promised >= actual else 0
    delay_hours = max(actual - promised, 0)

    return (hub_id, (delivered_cnt, on_time_cnt, delay_hours, delivery_charge))


# This merges values of same key within a partition.
def seq_func_delivery_metrics(acc, element) -> tuple[Any, Any, Any, Any]:
    return (
        acc[0] + element[0],
        acc[1] + element[1],
        acc[2] + element[2],
        acc[3] + element[3],
    )


# This merges values of same key in different partitions.
def comb_func_delivery_metrics(acc1, acc2):
    return (acc1[0] + acc2[0], acc1[1] + acc2[1], acc1[2] + acc2[2], acc1[3] + acc2[3])


def compute_kpis(item):
    hub_id, (metrics, hub_info) = item

    delivered_cnt, on_time_cnt, total_delay_hours, total_charge = metrics
    hub_city, region, manager, sla_target_pct = hub_info

    on_time_pct = (on_time_cnt / delivered_cnt) * 100.0 if delivered_cnt > 0 else 0.0
    avg_delay = (total_delay_hours / delivered_cnt) if delivered_cnt > 0 else 0.0
    sla_gap = on_time_pct - sla_target_pct
    target_status = "ACHIEVED" if sla_gap >= 0 else "NOT ACHIEVED"

    final_summary = {
        "hub_id": hub_id,
        "hub_city": hub_city,
        "region": region,
        "manager": manager,
        "delivered_count": delivered_cnt,
        "on_time_pct": on_time_pct,
        "avg_delay_hours": avg_delay,
        "total_charge": total_charge,
        "sla_target_pct": sla_target_pct,
        "sla_gap": sla_gap,
        "status": target_status,
    }
    return final_summary


def dict_to_csv_str(row_dict):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=row_dict.keys())
    writer.writerow(row_dict)
    return output.getvalue().strip()


if __name__ == "__main__":
    # ---------- Q1. Input path validation -----------
    ROOT_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = ROOT_DIR.joinpath(Path("data"))
    OUTPUT_DIR = ROOT_DIR.joinpath(Path("output/generated"))

    file_names = ["delivery_events.csv", "hub_master.csv"]
    file_paths = get_file_paths(file_names, DATA_DIR)
    file_exists_check = check_files_exist(file_paths)
    if all(file_exists_check):
        print(file_paths)
    else:
        missing_files = [
            file_path
            for file_path, exists in zip(file_paths, file_exists_check)
            if not exists
        ]
        raise FileNotFoundError(f"Missing files: {missing_files}")

    # ---------- Q2. Load data using RDDs -----------
    spark = SparkSession.builder.appName("Pyspark_RDD").master("local[*]").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    delivery_rdd, hub_rdd = load_files(file_paths)

    # ---------- Q3. Remove headers and blank rows -----------
    # ---------- Q4. Parse and validate events -----------
    delivery_rdd_cleaned, hub_rdd_cleaned = clean_rdds(
        [delivery_rdd, hub_rdd], file_names
    )

    # ---------- Q5. Split valid and rejected records -----------
    delivery_rdd_valid = delivery_rdd_cleaned.filter(lambda x: x["is_valid"]).map(
        lambda x: x["record"]
    )
    delivery_rdd_invalid = delivery_rdd_cleaned.filter(lambda x: not x["is_valid"])
    print(f"\nInvalid delivery records: {delivery_rdd_invalid.collect()}")

    hub_rdd_valid = hub_rdd_cleaned.filter(lambda x: x["is_valid"]).map(
        lambda x: x["record"]
    )
    hub_rdd_invalid = hub_rdd_cleaned.filter(lambda x: not x["is_valid"])
    print(f"\nInvalid hub records: {hub_rdd_invalid.collect()}")

    # ---------- Q6. Filter business-eligible records -----------
    delivery_rdd_delivered = delivery_rdd_valid.filter(
        lambda record: record["status"] == "DELIVERED"
    )

    # ---------- Q7. Create a pair rdd -----------
    delivery_pair_rdd = delivery_rdd_delivered.map(map_to_metrics)

    # ---------- Q8. Aggregate by hub -----------
    zero_value = (0, 0, 0, 0.0)
    metrics_rdd = delivery_pair_rdd.aggregateByKey(
        zero_value, seq_func_delivery_metrics, comb_func_delivery_metrics
    )
    print("\n--- Hub Level Aggregated Metrics ---")
    for hub_id, metrics in metrics_rdd.collect():
        print(
            f"Hub: {hub_id} -> Delivered: {metrics[0]}, On-Time: {metrics[1]}, Delay Hours: {metrics[2]}, Total Charges: ${metrics[3]:.2f}"
        )

    # ---------- Q9. Prepare the master Pair RDD -----------
    hub_pair_rdd = hub_rdd_valid.map(
        lambda record: (
            record["hub_id"],
            (
                record["hub_city"].title(),
                record["region"].title(),
                record["manager"].title(),
                float(record["sla_target_pct"]),
            ),
        )
    )
    # ---------- Q10. Join transactional and master data -----------
    joined_rdd = metrics_rdd.join(other=hub_pair_rdd)

    # ---------- Q11. Calculate final KPIs -----------
    kpis_rdd = joined_rdd.map(compute_kpis)

    # ---------- Q12. Sort the final report -----------
    sorted_rdd = kpis_rdd.sortBy(lambda item: item["on_time_pct"], ascending=False)
    print("\n==================== HUB SLA & PERFORMANCE REPORT ====================")
    for kpi in sorted_rdd.collect():
        print(
            f"Hub: {kpi['hub_id']} ({kpi['hub_city']}, {kpi['region']}) | Manager: {kpi['manager']}"
        )
        print(
            f"  -> Deliveries: {kpi['delivered_count']} | On-Time: {kpi['on_time_pct']:.1f}% (Target: {kpi['sla_target_pct']:.1f}%)"
        )
        print(
            f"  -> SLA Gap: {kpi['sla_gap']:+.1f}% | Performance Status: **{kpi['status']}**"
        )
        print(
            f"  -> Avg Delay: {kpi['avg_delay_hours']:.2f} hrs | Total Revenue: ${kpi['total_charge']:.2f}"
        )
        print("-" * 70)

    # ---------- Q13. Save the required output files -----------
    hub_report_output_dir = OUTPUT_DIR.joinpath("hub_sla_report/hub_sla_report.csv")
    rejected_output_dir = OUTPUT_DIR.joinpath(
        "rejected_delivery_events/rejected_delivery_events.csv"
    )

    for output_dir in [hub_report_output_dir, rejected_output_dir]:
        shutil.rmtree(output_dir, ignore_errors=True)

    sorted_rdd.coalesce(1).map(dict_to_csv_str).saveAsTextFile(
        str(hub_report_output_dir)
    )

    delivery_rdd_invalid.coalesce(1).map(dict_to_csv_str).saveAsTextFile(
        str(rejected_output_dir)
    )

    # ---------- Q14. Reload and verify saved output -----------
    output_file_paths = [hub_report_output_dir, rejected_output_dir]
    hub_report_rdd, invalid_deliveries_rdd = load_files(output_file_paths)

    print("\n==================== HUB SLA & PERFORMANCE REPORT ====================")
    for kpi in sorted_rdd.collect():
        print(
            f"Hub: {kpi['hub_id']} ({kpi['hub_city']}, {kpi['region']}) | Manager: {kpi['manager']}"
        )
        print(
            f"  -> Deliveries: {kpi['delivered_count']} | On-Time: {kpi['on_time_pct']:.1f}% (Target: {kpi['sla_target_pct']:.1f}%)"
        )
        print(
            f"  -> SLA Gap: {kpi['sla_gap']:+.1f}% | Performance Status: **{kpi['status']}**"
        )
        print(
            f"  -> Avg Delay: {kpi['avg_delay_hours']:.2f} hrs | Total Revenue: ${kpi['total_charge']:.2f}"
        )
        print("-" * 70)

    print(f"\nInvalid delivery records: {invalid_deliveries_rdd.collect()}")

    #  ---------- Q15. Reconciliation check -----------
    total_raw_count = delivery_rdd.count() - 1  # Subtract 1 for the header line

    technical_rejects_count = delivery_rdd_invalid.count()

    business_excluded_count = delivery_rdd_valid.filter(
        lambda record: record["status"] != "DELIVERED"
    ).count()

    kpi_transaction_count = delivery_pair_rdd.count()

    reconciled_total = (
        technical_rejects_count + business_excluded_count + kpi_transaction_count
    )
    variance = total_raw_count - reconciled_total

    print(
        "\n==================== DATA AUDIT BALANCE RECONCILIATION ===================="
    )
    print(f"Total Transactions Loaded (Input)    : {total_raw_count}")
    print(f"(-) Technical Rejects (Saved to CSV) : {technical_rejects_count}")
    print(f"(-) Business Excluded (Filtered Out) : {business_excluded_count}")
    print(f"(=) KPI Aggregated Deliveries        : {kpi_transaction_count}")
    print("---------------------------------------------------------------------------")
    print(f"Audit Balance Verification Total     : {reconciled_total}")
    print(f"Unaccounted Loss Variance            : {variance}")
    print("===========================================================================")
