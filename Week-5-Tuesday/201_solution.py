from pandas import DataFrame
import pandas as pd

if __name__ == "__main__":
    #part 1
    print("Part 1")
    df: DataFrame = pd.read_csv("transactions.csv", parse_dates=["txn_date"])
    print(df.shape)
    print(df.dtypes)
    print(df.isna().sum())

    #part 2
    print("Part 2")
    df["unit_price"] = df["unit_price"].fillna(df["unit_price"].mean())
    df["category"] = df["category"].fillna("Unknown")

    print(df.isna().sum())

    #part 3
    print("Part 3")
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["price_tier"] = "standard"
    df["price_tier"] = df["price_tier"].where(df["unit_price"] < 100, "premium")

    print(df.head())

    #part 4
    print("Part 4")
    filtered_electronics: DataFrame = df[(df["category"] == "Electronics") & (df["revenue"] > 500)]
    airport_mall_transactions: DataFrame = df.isin(["Airport", "Mall"])

    print(filtered_electronics.sum())
    print(airport_mall_transactions.sum())

    #Part 5
    print("Part 5")
