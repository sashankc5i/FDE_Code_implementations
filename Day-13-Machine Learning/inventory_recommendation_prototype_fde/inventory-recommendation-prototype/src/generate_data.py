from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 18

sku = [f"SKU-{1001+i}" for i in range(n)]
category = rng.choice(["Electronics", "Home", "Grocery"], n)
forecast = rng.integers(250, 1800, n)
inventory = rng.integers(50, 900, n)
safety_stock_pct = rng.choice([0.10, 0.15, 0.20], n)
unit_cost = rng.integers(20, 250, n)
moq = rng.choice([25, 50, 100, 200], n)
max_order = rng.integers(800, 2500, n)
budget = rng.integers(30000, 100000, n)
warehouse_capacity = rng.integers(800, 2500, n)

df = pd.DataFrame({
    "sku": sku,
    "category": category,
    "forecast_demand": forecast,
    "current_inventory": inventory,
    "safety_stock_pct": safety_stock_pct,
    "unit_cost": unit_cost,
    "moq": moq,
    "max_order": max_order,
    "budget": budget,
    "warehouse_capacity": warehouse_capacity,
})

out = Path(__file__).resolve().parents[1] / "data/raw/inventory_inputs.csv"
df.to_csv(out, index=False)
print(f"Wrote {out}")
