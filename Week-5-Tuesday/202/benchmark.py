import numpy as np
from numpy._core import records
import pandas as pd
from pathlib import Path
import os
import time

HERE = Path(__file__).parent

def make_df(n):
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "id": np.arange(n),
        "name": [f"user_{i}" for i in range(n)],
        "dept": rng.choice(["A", "B", "C", "D"], n),
        "score": rng.uniform(0, 100, n).round(3),
        "active": rng.choice([True, False], n),
        "ts": pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 1000, n), unit="h"),
    })

os.makedirs("out", exist_ok = True)

# ---------------------------------------------
# Part 1 
# ---------------------------------------------

def timed_write(label: str, path: str, fn):
    t = time.perf_counter()
    fn(path)
    secs = time.perf_counter() - t
    mb = os.path.getsize(path) / 1024 / 1024
    return f"{label:<8} {mb:7.2f} MB   {secs:6.3f} s"

test_cases = [
    ("CSV", "out/df.csv", lambda p: df.to_csv(p, index = False, date_format="%Y-%m-%dT%H:%M:%S")),
    ("JSONL", "out/df.jsonl", lambda p: df.to_json(p, orient = "records", lines = True, date_format = "iso")),
    ("Parquet", "out/df.parquet",lambda p: df.to_parquet(p, compression = "snappy"))
]

df = make_df(10000)

for label, path, write_fn in test_cases:
    print(timed_write(label, path, write_fn))

# ---------------------------------------------
# Part 2 
# ---------------------------------------------

def timed_write2(label: str, path: str, write_fn, read_fn):
    t = time.perf_counter()
    write_fn(path)
    write_s = time.perf_counter() - t
    mb = os.path.getsize(path) / 1024 / 1024
    
    t = time.perf_counter()
    read_fn(path)
    read_s = time.perf_counter() - t

    return {
        "format": label,
        "size_mb": round(mb, 2),
        "write_s": round(write_s, 3),
        "read_s": round(read_s, 3)
        }

def run_benchmark(n: int):
    df = make_df(n)
    cases = [
        ("CSV", f"out/df_{n}.csv", lambda p: df.to_csv(p, index = False, date_format = "iso"), lambda p: pd.read_csv(p, parse_dates = ["ts"])),
        ("JSONL", f"out/df_{n}.jsonl", lambda p: df.to_json(p, orient = "records", lines = True, date_format = "iso"), lambda p: pd.read_json(p, lines = True)),
        ("Parquet", f"out/df_{n}.parquet",lambda p: df.to_parquet(p, compression = "snappy"), lambda p: pd.read_parquet(p))
    ]
    rows = []
    for label, path, write_fn, read_fn in cases:
        row = timed_write2(label, path, write_fn, read_fn)
        row["rows"] = n
        rows.append(row)
    return pd.DataFrame(rows)

results = pd.concat(
    [run_benchmark(50_000), run_benchmark(500_000)],
    ignore_index= True
)

csv_sizes = (
    results.loc[results["format"] == "CSV"]
    .set_index("rows")["size_mb"]
)

results["vs_csv"] = (results["size_mb"] / results["rows"].map(csv_sizes)).round(2)
print("-" * 50)
print(f"Results:\n{results}")
print("-" * 50)

# ---------------------------------------------
# Part 3
# ---------------------------------------------

# compare dtypes of csv & parquet
csv_df = pd.read_csv(HERE / "out" / "df.csv")
parq_df = pd.read_parquet(HERE / "out" / "df.parquet")

print(csv_df.dtypes)
print("-" * 50)
print(parq_df.dtypes)