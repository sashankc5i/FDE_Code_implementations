import pandas as pd
import numpy as np


# -----------------------------------------
# 1. Load Topic 8 dataset
# -----------------------------------------

DATA_PATH = (
    "forecasting/"
    "data/demand_data.csv"
)

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)


# -----------------------------------------
# 2. Create business features
# -----------------------------------------

# Price change from previous day
df["price_change"] = (
    df["price"]
    .diff()
)


# Percentage price change
df["price_change_pct"] = (
    df["price"]
    .pct_change() * 100
)


# Promotion intensity
df["promotion_intensity"] = (
    df["promotion"]
)


# Promotion × price interaction
df["promotion_price_interaction"] = (
    df["promotion"]
    * df["price"]
)


# -----------------------------------------
# 3. Create calendar features
# -----------------------------------------

df["day_of_week"] = (
    df["date"].dt.dayofweek
)

df["month"] = (
    df["date"].dt.month
)

df["day_of_year"] = (
    df["date"].dt.dayofyear
)


# -----------------------------------------
# 4. Create trend
# -----------------------------------------

df["trend"] = np.arange(
    len(df)
)


# -----------------------------------------
# 5. Remove rows created by lag operation
# -----------------------------------------

df = df.dropna(
    subset=[
        "price_change",
        "price_change_pct"
    ]
).reset_index(drop=True)


# -----------------------------------------
# 6. Display dataset
# -----------------------------------------

print("\n========== DRIVER DATA ==========")

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)

print("\nColumns:")

print(
    df.columns.tolist()
)


# -----------------------------------------
# 7. Check missing values
# -----------------------------------------

print("\n========== MISSING VALUES ==========")

print(
    df.isna().sum()
)


# -----------------------------------------
# 8. Driver statistics
# -----------------------------------------

print("\n========== DRIVER SUMMARY ==========")

print(
    df[
        [
            "price",
            "price_change",
            "price_change_pct",
            "promotion",
            "holiday",
            "promotion_price_interaction"
        ]
    ].describe()
)


# -----------------------------------------
# 9. Save prepared dataset
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nPrepared data saved to: {OUTPUT_PATH}"
)