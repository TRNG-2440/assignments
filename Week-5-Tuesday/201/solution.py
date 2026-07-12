"""
solution script to 201 - data wrangling with pandas
"""
import pandas as pd
import numpy as np
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------
# Part 1 
# ---------------------------------------------

# load transactions
transactions = pd.read_csv(HERE / "transactions.csv", parse_dates = ["txn_date"])
print("-" * 50)
print(f"Transactions shape: {transactions.shape}")
print("-" * 50)
print(f"Data types of transactions columns:\n{transactions.dtypes}")
print("-" * 50)
print(f"Missing values per column of transactions:\n{transactions.isna().sum()}")
print("-" * 50)

# ---------------------------------------------
# Part 2
# ---------------------------------------------

# fill missing category values with Unknown
# fill missing unit_price with mean of corresponding category
transactions["category"] = transactions["category"].fillna("Unknown")
transactions["unit_price"] = transactions["unit_price"].fillna(transactions.groupby("category")["unit_price"].transform("mean"))

# print na values after updating
print(f"Missing values after updating:\n{transactions.isna().sum()}")
print("-" * 50)

# ---------------------------------------------
# Part 3
# ---------------------------------------------

# add revenue and price tier columns
transactions["revenue"] = (transactions["quantity"] * transactions["unit_price"]).round(2)
transactions["price_tier"] = np.where(transactions["unit_price"] >= 100, "premium", "standard")

# head transactions to show new columns
print(f"Transactions after adding revenue and price_tier:\n{transactions.head()}")
print("-" * 50)

# ---------------------------------------------
# Part 4
# ---------------------------------------------

# print eletronics transactions with revenue over 500 (along with count)
# count of transactions in Airport or Mall
elec_mask = (transactions["category"] == "Electronics") & (transactions["revenue"] > 500)
print(f"Electronics transactions with revenue > 500 (# of such transactions - {len(transactions.loc[elec_mask])}):\n{transactions.loc[elec_mask]}")
print("-" * 50)

airport_mall_mask = transactions["store"].isin(["Airport", "Mall"])
print(f"# of transactions in an airport or mall: {len(transactions.loc[airport_mall_mask])}")
print("-" * 50)

# ---------------------------------------------
# Part 5
# ---------------------------------------------

# aggregate values on category
txn_summary = (
    transactions.groupby("category")
    .agg(
        txns = ("txn_id", "count"),
        total_revenue = ("revenue", "sum"),
        avg_revenue = ("revenue", "mean")
    )
    .round(2)
    .reset_index()
    .sort_values("total_revenue", ascending = False)
)
print(f"Transaction summary:\n{txn_summary}")
print("-" * 50)

# ---------------------------------------------
# Part 6
# ---------------------------------------------

# merge total revenue per store, merge with stores.csv
stores = pd.read_csv(HERE / "stores.csv")
by_store = (
    transactions.groupby("store")["revenue"].sum()
    .reset_index()  # pyright: ignore[reportAttributeAccessIssue]
    .rename(columns = {"revenue": "actual"})
)
store_card = by_store.merge(stores, on = "store", how = "left")
store_card["revenue_per_rent"] = (store_card["actual"] / store_card["monthly_rent"]).round(3)
print(f"Merged dataframe with revenue_per_rent:\n{store_card}")
print("-" * 50)

# ---------------------------------------------
# Part 7
# ---------------------------------------------

# export transactions to parquet
parq_path = HERE / "transactions_clean.parquet"
transactions.to_parquet(parq_path, index = False)
print(f"Parquet file size: {parq_path.stat().st_size:,} bytes")

# read back with rows
transactions_clean = pd.read_parquet("transactions_clean.parquet")
print(f"Number of rows in transactions_clean: {transactions_clean.shape}")
print(f"txn_date data type: {transactions_clean["txn_date"].dtype}")