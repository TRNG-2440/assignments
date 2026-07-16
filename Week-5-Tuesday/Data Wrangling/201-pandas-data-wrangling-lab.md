Exercise 201 — Pandas Data Wrangling Lab
Overview
You'll take a raw, slightly messy CSV and run it through a full wrangling pipeline: load, inspect, clean, derive, filter, aggregate, merge, and export to Parquet. This is the bread-and-butter workflow you'll repeat for the rest of the week (BigQuery→DataFrame on Day 4, ETL on Day 5).

Write your work as a single runnable script (solution.py) that prints each part's deliverable. Reviewers run your script and check the printed output.

Learning Objectives
By the end you can independently:

Load a CSV and inspect it (info, dtypes, describe, isna)
Handle missing values deliberately (fillna, dropna)
Create derived columns (arithmetic + conditional)
Filter with boolean masks and .isin
Aggregate with groupby + agg and sort the result
Join a second table with merge
Export to Parquet and read it back
Exercise Mode
Guided but code-focused. Each part states exactly what to produce; the how is up to you. Lean on notes/201-pandas-refresher.md and demos/201-pandas-wrangling/ — the demo does the same moves on similar data, so use it as a worked reference (don't just copy it; the dataset and questions differ).

Prerequisites / Setup
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pandas pyarrow numpy
Generate your dataset — run this once to create the two CSVs you'll work with. (Deterministic seed, so everyone gets the same data and the same expected answers.)

# make_data.py  -- run: python make_data.py
import numpy as np, pandas as pd

rng = np.random.default_rng(2440)
N = 500
df = pd.DataFrame({
    "txn_id": np.arange(1, N + 1),
    "txn_date": pd.to_datetime("2026-01-01")
                + pd.to_timedelta(rng.integers(0, 90, N), unit="D"),
    "store": rng.choice(["Downtown", "Airport", "Mall", "Suburb"], N),
    "category": rng.choice(["Electronics", "Grocery", "Apparel", "Home"], N),
    "quantity": rng.integers(1, 8, N),
    "unit_price": rng.uniform(5, 200, N).round(2),
})
# Inject messiness: ~8% missing unit_price, a few missing categories.
df.loc[rng.choice(N, size=int(N * 0.08), replace=False), "unit_price"] = np.nan
df.loc[rng.choice(N, size=6, replace=False), "category"] = np.nan
df.to_csv("transactions.csv", index=False)

stores = pd.DataFrame({
    "store": ["Downtown", "Airport", "Mall", "Suburb"],
    "region": ["Central", "Central", "North", "South"],
    "monthly_rent": [12000, 20000, 15000, 8000],
})
stores.to_csv("stores.csv", index=False)
print("wrote transactions.csv (500 rows) and stores.csv (4 rows)")
You should end up with transactions.csv (500 rows, some missing values) and stores.csv (a 4-row lookup table).

Part 1 — Load & Inspect
Load transactions.csv (parse txn_date as a datetime). Print:

the shape,
dtypes,
the count of missing values per column (isna().sum()).
Deliverable: printed shape, dtypes, and per-column missing counts. Acceptance: txn_date shows dtype datetime64; missing counts show unit_price ≈ 40 and category = 6.

Part 2 — Handle Missing Values
Clean the two dirty columns:

Fill missing unit_price with the mean unit_price of that transaction's category (use groupby(...).transform("mean")).
Fill missing category with the literal string "Unknown".
Deliverable: print isna().sum() after cleaning. Acceptance: all columns report 0 missing values.

Part 3 — Derived Columns
Add:

revenue = quantity * unit_price, rounded to 2 decimals.
price_tier = "premium" when unit_price >= 100, else "standard" (use np.where).
Deliverable: print head() showing the new columns. Acceptance: revenue is numeric and equals quantity × unit_price; price_tier contains only "premium"/"standard".

Part 4 — Filter
Using boolean masks, produce and print:

all Electronics transactions with revenue > 500, and how many there are;
the count of transactions in either the Airport or Mall store (use .isin).
Deliverable: the filtered Electronics rows (or their count) + the isin count. Acceptance: filters use boolean masks / .isin (no Python for loops), and each condition is parenthesized when combined.

Part 5 — Aggregate
Build a per-category summary with groupby + agg:

txns = row count,
total_revenue = sum of revenue,
avg_revenue = mean revenue (rounded to 2).
reset_index() and sort by total_revenue descending.

Deliverable: the printed summary DataFrame. Acceptance: category is a normal column (not the index), rows are sorted descending by total_revenue, and columns are named exactly txns, total_revenue, avg_revenue.

Part 6 — Merge
Compute total revenue per store, then merge it with stores.csv on store (how="left"). Add a revenue_per_rent column = store_revenue / monthly_rent, rounded to 3.

Deliverable: the merged DataFrame with store, region, monthly_rent, store revenue, and revenue_per_rent. Acceptance: all 4 stores appear with their region and rent; revenue_per_rent is computed and finite.

Part 7 — Export to Parquet
Write the cleaned, enriched transactions DataFrame (from Part 3) to transactions_clean.parquet. Read it back and confirm the row count and that txn_date is still a datetime.

Deliverable: printed file size in bytes, the shape after read-back, and the txn_date dtype after read-back. Acceptance: the Parquet file exists, read-back shape matches, and txn_date comes back as datetime64 (not text) — proving Parquet preserved the type.

Definition of Done
solution.py runs top to bottom with python solution.py and no errors.
Every part prints a clearly labeled deliverable.
No Python for loops over rows — all transformations are vectorized pandas.
transactions_clean.parquet is produced by Part 7.
Submission
Submit make_data.py, solution.py, and the generated transactions_clean.parquet. Paste your full console output into your PR description.

Time Estimate
60–90 minutes.

Resources
notes/201-pandas-refresher.md
demos/201-pandas-wrangling/ — worked reference
pandas Comparison with SQL: https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html
Rubric (100 points)
Criterion	Points
Part 1 — load with correct dtypes + missing report	10
Part 2 — missing values handled correctly (group-mean + constant)	15
Part 3 — derived columns correct (revenue, price_tier)	15
Part 4 — mask + .isin filters, no loops	15
Part 5 — groupby/agg summary, reset_index, sorted, named correctly	15
Part 6 — merge + revenue_per_rent	15
Part 7 — Parquet export + type-preserving read-back	10
Script runs clean, deliverables clearly printed	5
Total	100
