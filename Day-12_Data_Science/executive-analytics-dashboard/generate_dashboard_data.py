import numpy as np
import pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)

# 24 months
months = pd.date_range("2024-01-01", "2025-12-01", freq="MS")

regions = ["North", "South", "East", "West"]
customer_types = ["Consumer", "SMB", "Enterprise"]

rows = []

for month_idx, month in enumerate(months):

    for region in regions:
        for customer_type in customer_types:

            # Base customer population
            customers = rng.integers(500, 1800)

            # Gradual business growth
            growth_factor = 1 + (month_idx * 0.012)

            customers = int(customers * growth_factor)

            # Orders per customer
            orders_per_customer = rng.normal(2.4, 0.25)

            orders = max(
                int(customers * orders_per_customer),
                customers
            )

            # AOV varies by customer type
            if customer_type == "Consumer":
                base_aov = 1400
            elif customer_type == "SMB":
                base_aov = 2300
            else:
                base_aov = 4200

            # Regional variation
            region_multiplier = {
                "North": 1.00,
                "South": 1.10,
                "East": 0.94,
                "West": 1.05
            }[region]

            aov = (
                base_aov
                * region_multiplier
                * (1 + rng.normal(0, 0.06))
            )

            revenue = orders * aov

            conversion = np.clip(
                rng.normal(0.072, 0.008),
                0.03,
                0.12
            )

            returns = np.clip(
                rng.normal(0.045, 0.01),
                0.015,
                0.09
            )

            retention = np.clip(
                rng.normal(0.82, 0.025),
                0.70,
                0.95
            )

            discount = np.clip(
                rng.normal(9, 2),
                2,
                18
            )

            rows.append({
                "month": month,
                "region": region,
                "customer_type": customer_type,
                "customers": customers,
                "orders": orders,
                "aov": round(aov, 2),
                "revenue": round(revenue, 2),
                "conversion_rate": round(conversion * 100, 2),
                "return_rate": round(returns * 100, 2),
                "retention_rate": round(retention * 100, 2),
                "discount_pct": round(discount, 2)
            })

df = pd.DataFrame(rows)

# Introduce a business event:
# South region starts experiencing increasing returns.
south_mask = df["region"] == "South"
later_period = df["month"] >= "2025-07-01"

df.loc[south_mask & later_period, "return_rate"] += np.linspace(
    2,
    7,
    (south_mask & later_period).sum()
)

# Revenue pressure in South during the same period.
df.loc[south_mask & later_period, "aov"] *= 0.97

df.loc[south_mask & later_period, "revenue"] = (
    df.loc[south_mask & later_period, "orders"]
    * df.loc[south_mask & later_period, "aov"]
)

# Save
output_dir = Path("executive-analytics-dashboard/data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "business_metrics.csv"

df.to_csv(output_path, index=False)

print("Dataset created:", output_path)
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nDate range:")
print(df["month"].min(), "to", df["month"].max())

print("\nPreview:")
print(df.head())