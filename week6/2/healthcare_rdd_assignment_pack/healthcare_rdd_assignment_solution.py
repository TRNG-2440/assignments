from typing import Any, Dict, Iterable

from pyspark import RDD, Accumulator, Broadcast
from pyspark.sql import SparkSession
from healthcare_rdd_assignment_starter import parse_line


def create_spark_session() -> SparkSession:
    spark: SparkSession = (
        SparkSession.builder.appName("RddHealthcareAssignment")
        .master("local[*]")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def part_a(spark: SparkSession) -> RDD[dict[str, Any]]:
    patient_visits: RDD[str] = spark.sparkContext.textFile("healthcare_patient_visits.csv", 2)
    header: str = patient_visits.first()
    patient_visits = patient_visits.filter(lambda line: line != header)
    return patient_visits.map(parse_line).cache()

def part_b(spark: SparkSession, rdd: RDD[dict[str, Any]]) -> RDD[dict[str, Any]]:
    missing_city_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    invalid_age_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    invalid_bill_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    invalid_status_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    invalid_total_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    allowed_statuses: set[str] = {"PAID", "PENDING", "CANCELLED"}
    
    def validate(record: Dict[str, Any]) -> bool:
        is_valid = True
        if not record["city"]:
            missing_city_acc.add(1)
            is_valid = False
        if record["age"] <= 0:
            invalid_age_acc.add(1)
            is_valid = False
        if record["bill_amount"] <= 0:
            invalid_bill_acc.add(1)
            is_valid = False
        if record["payment_status"] not in allowed_statuses:
            invalid_status_acc.add(1)
            is_valid = False
        if not is_valid:
            invalid_total_acc.add(1)
        return is_valid

    valid_rdd: RDD[dict[str, Any]] = rdd.filter(validate)
    print("missing_cities:", missing_city_acc.value)
    print("invalid_ages:", invalid_age_acc.value)
    print("invalid_bills:", invalid_bill_acc.value)
    print("invalid_statuses:", invalid_status_acc.value)
    print("invalid_total:", invalid_total_acc.value)
    return valid_rdd

def part_c(spark: SparkSession, rdd: RDD[dict[str, Any]]) -> RDD[dict[str, Any]]:
    service_charge_map = {
        "Cardiology": 0.18,
        "Orthopedics": 0.12,
        "Dermatology": 0.08,
        "Neurology": 0.15,
        "General Medicine": 0.05,
    }
    service_charge_bc: Broadcast[dict[str, float]] = spark.sparkContext.broadcast(service_charge_map)

    def enrich(record: Dict[str, Any]) -> Dict[str, Any]:
        pct: float = service_charge_bc.value.get(record["department"], 0.0)
        service_charge: float = record["bill_amount"] * pct
        final_amount: float = record["bill_amount"] + service_charge
        return {
            **record,
            "service_charge_pct": pct,
            "service_charge": round(service_charge, 2),
            "final_amount": round(final_amount, 2),
        }
    return rdd.map(enrich)

def part_d(spark: SparkSession, rdd: RDD[dict[str, Any]]) -> None:
    #map used in part_c
    paid_records: RDD[dict[str, Any]] = rdd.filter(lambda record: record["payment_status"] == "PAID")
    print("filter -> paid records", paid_records.take(5))
    search_tags: RDD[dict[str, Any]] = rdd.map(lambda record: {"patient_id": record["patient_id"], "search_tag": f"{record['department']}_{record['city']}"})
    print("map -> search tags", search_tags.take(5))
    distinct_cities: RDD[dict[str, Any]] = rdd.map(lambda record: record["city"]).distinct()
    distinct_departments: RDD[dict[str, Any]] = rdd.map(lambda record: record["department"]).distinct()
    print("distinct -> unique cities", distinct_cities.collect())
    print("distinct -> unique departments", distinct_departments.collect())
    amounts_formatted: RDD[tuple[str, str]] = rdd.map(lambda record: (record["patient_id"], record["final_amount"])).mapValues(lambda amount: f"${amount:.2f}")
    print("mapValues -> formatted amounts", amounts_formatted.take(5))
    city_revenue: RDD[tuple[str, float]] = paid_records.map(lambda record: (record["city"], record["final_amount"])).reduceByKey(lambda a, b: a + b)
    print("reduceByKey -> city revenue", city_revenue.collect())
    department_revenue: RDD[tuple[str, float]] = paid_records.map(lambda record: (record["department"], record["final_amount"])).reduceByKey(lambda a, b: a + b)
    print("reduceByKey -> department revenue", department_revenue.collect())
    vist_ids_by_department: RDD[tuple[str, Iterable[str]]] = rdd.map(lambda record: (record["department"], record["patient_id"])).groupByKey()
    print("groupByKey -> visit ids by department", vist_ids_by_department.collect())
    sorted_department_revenue: RDD[tuple[str, float]] = department_revenue.sortBy(lambda record: record[1], ascending=False)
    print("sortBy -> sorted department revenue", sorted_department_revenue.collect())
    opd_patients: RDD[str] = (rdd.filter(lambda r: r["visit_type"] == "OPD")
                                .map(lambda r: r["patient_id"]))
    
    emergency_patients: RDD[str] = (rdd.filter(lambda r: r["visit_type"] == "Emergency")
                                    .map(lambda r: r["patient_id"]))
    print("union -> OPD + Emergency patients", opd_patients.union(emergency_patients).distinct().collect())
    print("Repartition + Coalesced")
    print("Original:", rdd.getNumPartitions())
    print("Repartitioned:", rdd.repartition(6).getNumPartitions())
    print("Coalesced:", rdd.repartition(6).coalesce(2).getNumPartitions())

def part_e(spark: SparkSession, base_rdd: RDD[dict[str, Any]], enriched_rdd: RDD[dict[str, Any]]) -> None:
    paid_records: RDD[dict[str, Any]] = enriched_rdd.filter(lambda record: record["payment_status"] == "PAID")
    print("count -> total data rows", base_rdd.count())
    print("first -> first enriched record", enriched_rdd.first())
    print("take -> first 5 enriched records", enriched_rdd.take(5))
    print("collect -> distinct cities", enriched_rdd.map(lambda record: record["city"]).distinct().collect())
    print("countByValue -> visits by department", enriched_rdd.map(lambda record: record["department"]).countByValue())
    print("reduce -> total paid revenue", paid_records.map(lambda record: record["final_amount"]).reduce(lambda a, b: a + b))
    print("takeOrdered -> 3 lowest bill amounts", enriched_rdd.takeOrdered(3, key=lambda record: record["bill_amount"]))

    positive_bill_acc: Accumulator[int] = spark.sparkContext.accumulator(0)
    def check_positive_bill(record: Dict[str, Any]) -> None:
        if record["bill_amount"] > 0:
            positive_bill_acc.add(1)
    enriched_rdd.foreach(check_positive_bill)
    print("foreach -> records with positive bill amount", positive_bill_acc.value)

def part_f(spark: SparkSession, base_rdd: RDD[dict[str, Any]], valid_rdd: RDD[dict[str, Any]], enriched_rdd: RDD[dict[str, Any]]) -> None:
    paid_records: RDD[dict[str, Any]] = enriched_rdd.filter(lambda record: record["payment_status"] == "PAID")
    total_rows: int = base_rdd.count()
    valid_rows: int = valid_rdd.count()
    print("1. total data rows ->", total_rows)
    print("2. valid rows / invalid rows ->", valid_rows, total_rows - valid_rows)

    print("3. visits by city ->", enriched_rdd.map(lambda record: record["city"]).countByValue())
    print("4. visits by department ->", enriched_rdd.map(lambda record: record["department"]).countByValue())
    city_revenue: RDD[tuple[str, float]] = paid_records.map(lambda record: (record["city"], record["final_amount"])).reduceByKey(lambda a, b: a + b)
    print("5. final revenue by city ->", city_revenue.collect())
    department_revenue: RDD[tuple[str, float]] = paid_records.map(lambda record: (record["department"], record["final_amount"])).reduceByKey(lambda a, b: a + b)
    print("6. final revenue by department ->", department_revenue.collect())
    print("7. top 3 paid visits by final amount ->", paid_records.takeOrdered(3, key=lambda record: -record["final_amount"]))
    emergency_departments: RDD[str] = enriched_rdd.filter(lambda record: record["visit_type"] == "Emergency").map(lambda record: record["department"]).distinct()
    print("8. departments handling emergency visits ->", emergency_departments.collect())
    print("9. distinct cities ->", enriched_rdd.map(lambda record: record["city"]).distinct().collect())
    print("9. distinct departments ->", enriched_rdd.map(lambda record: record["department"]).distinct().collect())
    rating_totals: RDD[tuple[str, tuple[int, int]]] = (
        enriched_rdd.map(lambda record: (record["department"], (record["rating"], 1)))
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))
    )
    average_ratings: RDD[tuple[str, float]] = rating_totals.mapValues(lambda totals: totals[0] / totals[1])
    top_rated_department: tuple[str, float] = average_ratings.sortBy(lambda record: record[1], ascending=False).first()
    print("10. department with highest average rating ->", top_rated_department)

if __name__ == "__main__":
    spark = create_spark_session()
    try:
        print("Part A")
        base_rdd: RDD[dict[str, Any]] = part_a(spark)
        print("Part B")
        valid_rdd: RDD[dict[str, Any]] = part_b(spark, base_rdd)
        print("Part C")
        enriched_rdd: RDD[dict[str, Any]] = part_c(spark, valid_rdd)
        print("Part D")
        part_d(spark, enriched_rdd)
        print("Part E")
        part_e(spark, base_rdd, enriched_rdd)
        print("Part F")
        part_f(spark, base_rdd, valid_rdd, enriched_rdd)
    except Exception as e:
        print(e)
        exit(1)
    finally:
        spark.stop()