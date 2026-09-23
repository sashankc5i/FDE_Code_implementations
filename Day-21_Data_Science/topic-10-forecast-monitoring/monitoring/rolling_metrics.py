import pandas as pd
import numpy as np


# -----------------------------------------
# 1. Load variance data
# -----------------------------------------

DATA_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/variance_analysis.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Sort chronologically
# -----------------------------------------

df = df.sort_values(
    "date"
).reset_index(
    drop=True
)


# -----------------------------------------
# 3. Calculate rolling metrics
# -----------------------------------------

WINDOW = 7


df["rolling_mae"] = (
    df["absolute_error"]
    .rolling(WINDOW)
    .mean()
)


df["rolling_rmse"] = (
    df["error"]
    .pow(2)
    .rolling(WINDOW)
    .mean()
    .apply(np.sqrt)
)


df["rolling_bias"] = (
    df["error"]
    .rolling(WINDOW)
    .mean()
)


df["rolling_variance_pct"] = (
    df["variance_pct"]
    .rolling(WINDOW)
    .mean()
)


# -----------------------------------------
# 4. Determine rolling bias direction
# -----------------------------------------

def bias_direction(value):

    if pd.isna(value):
        return "Insufficient Data"

    if value > 0:
        return "Overperformance"

    elif value < 0:
        return "Underperformance"

    return "Neutral"


df["rolling_bias_direction"] = (
    df["rolling_bias"]
    .apply(bias_direction)
)


# -----------------------------------------
# 5. Print summary
# -----------------------------------------

print(
    "\n========== ROLLING METRICS =========="
)

print(
    f"Rolling window: {WINDOW} days"
)


print(
    "\nLatest rolling metrics:"
)

print(
    df[
        [
            "date",
            "rolling_mae",
            "rolling_rmse",
            "rolling_bias",
            "rolling_variance_pct",
            "rolling_bias_direction"
        ]
    ]
    .tail(10)
    .to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 6. Overall rolling summary
# -----------------------------------------

valid = df[
    df["rolling_mae"].notna()
].copy()


print(
    "\n========== ROLLING SUMMARY =========="
)

print(
    f"Average rolling MAE: "
    f"{valid['rolling_mae'].mean():.4f}"
)

print(
    f"Average rolling RMSE: "
    f"{valid['rolling_rmse'].mean():.4f}"
)

print(
    f"Average rolling bias: "
    f"{valid['rolling_bias'].mean():.4f}"
)

print(
    f"Minimum rolling bias: "
    f"{valid['rolling_bias'].min():.4f}"
)

print(
    f"Maximum rolling bias: "
    f"{valid['rolling_bias'].max():.4f}"
)


# -----------------------------------------
# 7. Save rolling metrics
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/rolling_metrics.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nRolling metrics saved to: {OUTPUT_PATH}"
)