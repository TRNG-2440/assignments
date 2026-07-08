import pandas as pd
import numpy as np
import os

# 201 Pandas
# Part 1
print("---- Part 1 ----")

# Read CSV and parse txn_date to datetime
df = pd.read_csv("transactions.csv", parse_dates=["txn_date"])

# Get shape (rows, columns)
print(f"Shape: {df.shape}")

# Get data types for each column
print(f"Date Types:{df.dtypes}")

# Get the number of missing values in each column
print(f"# of missing values: {df.isna().sum()}")

# Part 2
print("---- Part 2 ----")

# Fill missing values with unknown
df["category"] = df["category"].fillna("Unknown")

# Fill missing values with unit_price mean
df["unit_price"] = df["unit_price"].fillna(
    df.groupby("category")["unit_price"].transform("mean")
)

print(f"# of missing values after filling:\n{df.isna().sum()}")

# Part 3
print("---- Part 3 ----")


# New column revenue
df["revenue"] = df["quantity"] * df["unit_price"]

#New column price_tier
df["price_tier"] = np.where(df["unit_price"] >= 100, "premium", "standard")

print(f"Printing head of new revenue and price_tier added: {df.head()}")

# Part 4
print("---- Part 4 ----")


# Mask for electronics and revenue > 500
print(f"Mask with electronis and revenue >50: {df[(df["category"] == "Electronics") & (df["revenue"] > 500)]}")

# Mask for airport and mall stores
mask = df["store"].isin(["Airport", "Mall"])

# Shows the count of rows in the mask
print(f"Count of rows in mask: {mask.sum()}")

# Part 5
print("---- Part 5 ----")

# Per category summary
category_summary = df.groupby("category").agg(
        txns = ("txn_id", "count"),
        total_revenue = ("revenue", "sum"),
        avg_revenue = ("revenue", "mean")
    ).reset_index()

# Round the avg_revenue to 2 decimal places
category_summary["avg_revenue"] = category_summary["avg_revenue"].round(2)

# Sort total_revenue in DESC
category_summary = category_summary.sort_values("total_revenue", ascending=False)

print(f"Category Summary:\n{category_summary}")

# Part 6
print("---- Part 6 ----")

# Get store revenue sum
store_revenue = df.groupby("store").agg(
    store_revenue = ("revenue", "sum")
).reset_index()

# Read store.csv
stores = pd.read_csv("stores.csv")

# Merge stores with store_revenue based on store column
store_summary = stores.merge(store_revenue, on="store", how="left")

# New column with revenue_per_rent
store_summary["revenue_per_rent"] = (store_summary["store_revenue"] / store_summary["monthly_rent"]).round(3)

print(f"New columns for store.csv:\n {store_summary}")

# Part 7
print("---- Part 7 ----")

# Change to parquet
df.to_parquet("transactions_clean.parquet", index=False)

# Get file size
file_size = os.path.getsize("transactions_clean.parquet")
print(f"Parquet file size (bytes): {file_size}")

# Read parquet
df_parquet = pd.read_parquet("transactions_clean.parquet")

print(f"Read-back shape: {df_parquet.shape}")
print(f"txn_date dtype after read-back: {df_parquet['txn_date'].dtype}")