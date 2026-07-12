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