import pandas as pd
import numpy as np


# -----------------------------------------
# 1. Load rolling metrics
# -----------------------------------------

DATA_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/rolling_metrics.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Configuration
# -----------------------------------------

WINDOW = 14
Z_THRESHOLD = 2.0


# -----------------------------------------
# 3. Calculate rolling error statistics
# -----------------------------------------

df["error_mean_rolling"] = (
    df["error"]
    .rolling(WINDOW)
    .mean()
)


df["error_std_rolling"] = (
    df["error"]
    .rolling(WINDOW)
    .std()
)


# -----------------------------------------
# 4. Calculate rolling z-score
# -----------------------------------------

df["error_zscore"] = (
    (
        df["error"]
        - df["error_mean_rolling"]
    )
    /
    df["error_std_rolling"].replace(
        0,
        np.nan
    )
)


# -----------------------------------------
# 5. Identify anomalies
# -----------------------------------------

df["is_anomaly"] = (
    df["error_zscore"].abs()
    >= Z_THRESHOLD
)


# -----------------------------------------
# 6. Classify anomaly direction
# -----------------------------------------

def anomaly_direction(row):

    if not row["is_anomaly"]:
        return "Normal"

    if row["error"] > 0:
        return "Positive Anomaly"

    return "Negative Anomaly"


df["anomaly_type"] = (
    df.apply(
        anomaly_direction,
        axis=1
    )
)


# -----------------------------------------
# 7. Print anomaly summary
# -----------------------------------------

print(
    "\n========== ANOMALY DETECTION =========="
)

print(
    f"Rolling window: {WINDOW} days"
)

print(
    f"Z-score threshold: ±{Z_THRESHOLD}"
)


anomaly_count = (
    df["is_anomaly"]
    .sum()
)


print(
    f"Anomalies detected: {anomaly_count}"
)


# -----------------------------------------
# 8. Show anomalies
# -----------------------------------------

anomalies = df[
    df["is_anomaly"]
].copy()


print(
    "\n========== DETECTED ANOMALIES =========="
)


if len(anomalies) == 0:

    print(
        "No anomalies detected."
    )

else:

    print(
        anomalies[
            [
                "date",
                "actual_demand",
                "forecast_demand",
                "error",
                "variance_pct",
                "error_zscore",
                "anomaly_type"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )


# -----------------------------------------
# 9. Save anomaly results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/anomaly_detection.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nAnomaly analysis saved to: {OUTPUT_PATH}"
)