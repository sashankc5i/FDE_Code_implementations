import pandas as pd


# -----------------------------------------
# 1. Load prepared driver data
# -----------------------------------------

DATA_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

df = pd.read_csv(DATA_PATH)


# -----------------------------------------
# 2. Select candidate drivers
# -----------------------------------------

DRIVERS = [
    "price",
    "price_change",
    "price_change_pct",
    "promotion",
    "holiday",
    "promotion_price_interaction",
    "day_of_week",
    "month",
    "day_of_year",
    "trend"
]


# -----------------------------------------
# 3. Calculate correlations
# -----------------------------------------

correlations = (
    df[
        DRIVERS + ["demand"]
    ]
    .corr()["demand"]
    .drop("demand")
    .sort_values(
        key=lambda x: x.abs(),
        ascending=False
    )
)


# -----------------------------------------
# 4. Convert to DataFrame
# -----------------------------------------

correlation_df = (
    correlations
    .reset_index()
)

correlation_df.columns = [
    "feature",
    "correlation"
]


# -----------------------------------------
# 5. Add absolute correlation
# -----------------------------------------

correlation_df["absolute_correlation"] = (
    correlation_df["correlation"].abs()
)


# -----------------------------------------
# 6. Print results
# -----------------------------------------

print(
    "\n========== DEMAND DRIVER RELATIONSHIPS =========="
)

print(
    correlation_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 7. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/driver_correlations.csv"
)

correlation_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nCorrelation results saved to: "
    f"{OUTPUT_PATH}"
)