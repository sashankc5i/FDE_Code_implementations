import numpy as np
import pandas as pd


np.random.seed(42)


# -----------------------------------------
# 1. Create daily time-series dates
# -----------------------------------------

dates = pd.date_range(
    start="2023-01-01",
    end="2025-12-31",
    freq="D"
)

df = pd.DataFrame({
    "date": dates
})


# -----------------------------------------
# 2. Create calendar features
# -----------------------------------------

df["day_of_week"] = df["date"].dt.dayofweek
df["month"] = df["date"].dt.month


# -----------------------------------------
# 3. Create underlying business patterns
# -----------------------------------------

# Long-term growth
df["trend"] = np.arange(len(df)) * 0.05


# Weekly seasonality
df["weekly_seasonality"] = (
    100
    + 20 * np.sin(
        2 * np.pi * df["day_of_week"] / 7
    )
)


# -----------------------------------------
# 4. Business drivers
# -----------------------------------------

# Product price
df["price"] = (
    100
    + 5 * np.sin(
        2 * np.pi * df["month"] / 12
    )
    + np.random.normal(
        0,
        2,
        len(df)
    )
)


# Promotion
df["promotion"] = (
    np.random.random(len(df)) < 0.15
).astype(int)


# Holiday indicator
df["holiday"] = (
    df["month"].isin([11, 12])
    & (df["day_of_week"] >= 5)
).astype(int)


# -----------------------------------------
# 5. Random noise
# -----------------------------------------

noise = np.random.normal(
    0,
    15,
    len(df)
)


# -----------------------------------------
# 6. Generate demand
# -----------------------------------------

df["demand"] = (
    500
    + df["trend"]
    + df["weekly_seasonality"]
    - 3 * df["price"]
    + 80 * df["promotion"]
    + 50 * df["holiday"]
    + noise
)


# Demand cannot be negative
df["demand"] = df["demand"].clip(
    lower=0
)


# -----------------------------------------
# 7. Keep observed business columns
# -----------------------------------------

df = df[
    [
        "date",
        "demand",
        "price",
        "promotion",
        "holiday"
    ]
]


# -----------------------------------------
# 8. Save dataset
# -----------------------------------------

output_path = (
    "forecasting/"
    "data/demand_data.csv"
)

df.to_csv(
    output_path,
    index=False
)


print("Dataset generated successfully.")
print(f"Rows: {len(df)}")
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset summary:")
print(df.describe())