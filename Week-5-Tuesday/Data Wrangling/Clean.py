import os

import numpy as np
import pandas as pd

# Part 1 — Load and Inspect data
print(f'\n{'-' * 20} Part 1 — Load and Inspect{'-' * 20}\n')

# Read from csv file
df = pd.read_csv("transactions.csv", parse_dates=["txn_date"])

# Displays size of table
print("Shape:", df.shape)

# Displays data type of each column
print("\nData types: ", df.dtypes)

# Show missing values for each column
print("\nMissing values per column:", df.isna().sum())

# Part 2 — Handle Missing Values
print(f'\n{'-' * 20} Part 2 — Handle missing values{'-' * 20}\n')

# Fill empty category values with 'Unknown' first (needed for group mean below)
df["category"] = df["category"].fillna("Unknown")

# Fill missing unit_price with the mean unit_price of that row's category
df["unit_price"] = df["unit_price"].fillna(df.groupby("category")["unit_price"].transform("mean"))

print("Sum of missing values after cleaning:")
print(df.isna().sum())

# Part 3 — Derived Columns
print(f'\n{'-' * 20} Part 3 — Derived Columns{'-' * 20}\n')

# Round 2 decimals for "revenue" column
df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)

# If df["price_tier"] is >= 100 assign value of price_tier to "premium", other assign value to "standard"
df["price_tier"] = np.where(df["unit_price"] >= 100, "premium", "standard")

# Print first 5 values
print(df.head())

# Part 4 — Filter
print(f'\n{'-' * 20} Part 4 — Filter{'-' * 20}\n')

# Declare electronic data frame that contains elentronics with revenue greater than $500
electronicDataFrame = df[(df["category"] == "Electronics") & (df["revenue"] > 500)]

# Display size of electronic data frame
print(f"Electronics transactions with revenue > 500: {len(electronicDataFrame)}")

# Display entire electronic data frame
print(electronicDataFrame)

# Determine amount of transactions in airport or mall
airportOrMall = df[df["store"].isin(["Airport", "Mall"])].shape[0]
print(f"\nTransactions in Airport or Mall: {airportOrMall}")

# Part 5 — Aggregate
print(f'\n{'-' * 20} Part 5 — Aggregate{'-' * 20}\n')

# Declare category data frame that groups by category, then for 
# each category counts by transaction, sum revenue and average revenue
categoryDataFrame = (
    df.groupby("category")
    .agg(
        transactions=("revenue", "count"),
        total_revenue=("revenue", "sum"),
        avg_revenue=("revenue", "mean"),
    )
    .reset_index()
)

# Round average revenue by 2 decimals
categoryDataFrame["avg_revenue"] = categoryDataFrame["avg_revenue"].round(2)

# Sort dataframe by highest to lowest based on total revenue
categorySummary = categoryDataFrame.sort_values("total_revenue", ascending=False)

# Display dataframe which consists of all metrics
print(categorySummary.to_string(index=False))

# Part 6 — Merge
print(f'\n{'-' * 20} Part 6 — Merge{'-' * 20}\n')

# Declare dataframe that groups by store
store_revenue = (
    df.groupby("store", as_index=False)
    .agg(store_revenue=("revenue", "sum"))
)

# Read from stores.csv file
stores = pd.read_csv("stores.csv")

# Merge store revenue with store details (region, rent) on store name
merged = store_revenue.merge(stores, on="store", how="left")

# Calculate revenue earned per dollar of monthly rent 
merged["revenue_per_rent"] = (merged["store_revenue"] / merged["monthly_rent"]).round(3)

# Print merged dataframe
print(merged.to_string(index=False))

# Part 7 — Export to Parquet
print(f'\n{'-' * 20} Part 7 — Export to Parquet{'-' * 20}\n')

# Declare name of parquet file
parquetPath = "transactions_clean.parquet"

# Export dataframe to parquet file
df.to_parquet(parquetPath, index=False)

# Determine file size of parquet file
file_size = os.path.getsize(parquetPath)

# Import content from parquet back to 
dataFrameParquet = pd.read_parquet(parquetPath)

# Display file size in bytes
print(f"File size (bytes): {file_size}")

# Display shape after data wrangling operation is complete
print(f"Shape after read-back: {dataFrameParquet.shape}")

# Confirm parquet dates are real dates
print(f"txn_date dtype after read-back: {dataFrameParquet['txn_date'].dtype}")
