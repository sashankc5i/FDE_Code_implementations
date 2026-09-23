import pandas as pd
import numpy as np


# -----------------------------------------
# 1. Load monitoring data
# -----------------------------------------

DATA_PATH = (
    "topic-10-forecast-monitoring/"
    "data/monitoring_data.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Keep rows where both exist
# -----------------------------------------

df = df[
    df["actual_demand"].notna()
    & df["forecast_demand"].notna()
].copy()


# -----------------------------------------
# 3. Recalculate error
# -----------------------------------------

df["error"] = (
    df["actual_demand"]
    - df["forecast_demand"]
)


# -----------------------------------------
# 4. Absolute error
# -----------------------------------------

df["absolute_error"] = (
    df["error"].abs()
)


# -----------------------------------------
# 5. Variance percentage
# -----------------------------------------

df["variance_pct"] = (
    df["error"]
    / df["forecast_demand"].replace(
        0,
        np.nan
    )
) * 100


# -----------------------------------------
# 6. Absolute variance percentage
# -----------------------------------------

df["absolute_variance_pct"] = (
    df["variance_pct"].abs()
)


# -----------------------------------------
# 7. Classify severity
# -----------------------------------------

def classify_severity(variance):

    if pd.isna(variance):
        return "Unknown"

    variance = abs(variance)

    if variance <= 5:
        return "Normal"

    elif variance <= 10:
        return "Watch"

    elif variance <= 20:
        return "Warning"

    else:
        return "Critical"


df["severity"] = (
    df["variance_pct"]
    .apply(classify_severity)
)


# -----------------------------------------
# 8. Determine direction
# -----------------------------------------

def determine_direction(error):

    if pd.isna(error):
        return "Unknown"

    if error > 0:
        return "Above Forecast"

    elif error < 0:
        return "Below Forecast"

    else:
        return "On Forecast"


df["direction"] = (
    df["error"]
    .apply(determine_direction)
)


# -----------------------------------------
# 9. Summary metrics
# -----------------------------------------

mae = df["absolute_error"].mean()

rmse = np.sqrt(
    np.mean(
        df["error"] ** 2
    )
)

bias = df["error"].mean()

mean_variance = (
    df["variance_pct"].mean()
)


# -----------------------------------------
# 10. Print metrics
# -----------------------------------------

print(
    "\n========== VARIANCE ANALYSIS =========="
)

print(
    f"Rows monitored: {len(df)}"
)

print(
    f"MAE: {mae:.4f}"
)

print(
    f"RMSE: {rmse:.4f}"
)

print(
    f"Bias: {bias:.4f}"
)

print(
    f"Mean Variance %: {mean_variance:.4f}%"
)


# -----------------------------------------
# 11. Severity distribution
# -----------------------------------------

print(
    "\n========== SEVERITY DISTRIBUTION =========="
)

severity_counts = (
    df["severity"]
    .value_counts()
    .reindex(
        [
            "Normal",
            "Watch",
            "Warning",
            "Critical"
        ],
        fill_value=0
    )
)

print(
    severity_counts
)


# -----------------------------------------
# 12. Direction distribution
# -----------------------------------------

print(
    "\n========== DIRECTION DISTRIBUTION =========="
)

print(
    df["direction"].value_counts()
)


# -----------------------------------------
# 13. Save detailed monitoring output
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/variance_analysis.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nVariance analysis saved to: {OUTPUT_PATH}"
)