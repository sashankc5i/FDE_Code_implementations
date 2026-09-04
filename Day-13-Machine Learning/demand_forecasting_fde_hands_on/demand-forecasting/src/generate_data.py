import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
n_days = 420
dates = pd.date_range("2025-01-01", periods=n_days, freq="D")

df = pd.DataFrame({"date": dates})
t = np.arange(n_days)

# Structural demand: trend + weekly seasonality + recurring campaign effects
trend = 180 + 0.30 * t
weekly = 28 * np.sin(2 * np.pi * t / 7)
monthly = 12 * np.sin(2 * np.pi * t / 30.5)

promotion = (
    ((df["date"].dt.dayofweek >= 4) & (df["date"].dt.dayofweek <= 6))
    & (df["date"].dt.day % 5 == 0)
).astype(int)

holiday = (
    ((df["date"].dt.month == 11) & (df["date"].dt.day >= 20))
    | ((df["date"].dt.month == 12) & (df["date"].dt.day <= 31))
).astype(int)

true_demand = (
    trend
    + weekly
    + monthly
    + 45 * promotion
    + 30 * holiday
    + rng.normal(0, 12, n_days)
)

# Simulate operational constraints: some observed sales are capped by inventory.
stockout = rng.random(n_days) < 0.035
capacity = np.where(stockout, true_demand * rng.uniform(0.55, 0.80, n_days), true_demand)
observed_demand = np.maximum(0, np.round(capacity)).astype(int)

df["promotion"] = promotion
df["holiday"] = holiday
df["stockout"] = stockout.astype(int)
df["demand"] = observed_demand

out = Path(__file__).resolve().parents[1] / "data/raw/demand.csv"
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f"Wrote {out}")
