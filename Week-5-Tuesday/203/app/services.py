"""
Service Layer
"""
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).parent.parent / "data" / "transactions.csv"

DF: pd.DataFrame | None = None

def load_data() -> pd.DataFrame:
    global DF
    if DF is None:
        df = pd.read_csv(DATA_FILE, parse_dates = ["txn_date"])
        df["revenue"] = (df["unit_price"] * df["quantity"]).round(2)
        DF = df
    return DF

def records(df: pd.DataFrame) -> list[dict]:
    df = df.copy()
    if "txn_date" in df.columns:
        df["txn_date"] = df["txn_date"].dt.strftime("%Y-%m-%d")
    return df.where(df.notna(), None).to_dict(orient = "records")

def summary() -> dict:
    df = load_data()
    return {
        "transactions": int(len(df)),
        "total_revenue": round(float(df["revenue"].sum()), 2), # pyright: ignore[reportArgumentType]
        "avg_txn_revenue": round(float(df["revenue"].mean()), 2), # pyright: ignore[reportArgumentType]
        "stores": int(df["store"].nunique()), # pyright: ignore[reportArgumentType]
        "categories": int(df["category"].nunique()) # pyright: ignore[reportArgumentType]
    }

def by_category() -> list[dict]:
    df = load_data()
    agg = (
        df.groupby("category")
        .agg(transactions=("txn_id", "count"),
             total_revenue=("revenue", "sum"),
             avg_revenue=("revenue", "mean"))
        .round(2)
        .reset_index()
        .sort_values("total_revenue", ascending = False)
    )
    return records(agg)

def transactions_page(limit: int, offset: int, store: str | None) -> dict:
    df = load_data()
    if store:
        df = df[df["store"] == store]
    total = len(df)
    page = df.iloc[offset: offset + limit]
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": records(page)
    }