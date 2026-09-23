import pandas as pd
import numpy as np


# -----------------------------------------
# 1. Load historical forecast
# -----------------------------------------

FORECAST_PATH = (
    "forecasting/"
    "outputs/forecast_with_intervals.csv"
)

df = pd.read_csv(
    FORECAST_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Calculate forecast error
# -----------------------------------------

df["error"] = (
    df["demand"]
    - df["forecast"]
)


df["absolute_error"] = (
    df["error"].abs()
)


# -----------------------------------------
# 3. Check prediction interval
# -----------------------------------------

df["inside_interval"] = (
    (
        df["demand"] >= df["lower_bound"]
    )
    &
    (
        df["demand"] <= df["upper_bound"]
    )
)


# -----------------------------------------
# 4. Calculate distance from interval
# -----------------------------------------

df["interval_distance"] = np.where(
    df["demand"] < df["lower_bound"],
    df["demand"] - df["lower_bound"],
    np.where(
        df["demand"] > df["upper_bound"],
        df["demand"] - df["upper_bound"],
        0
    )
)


# -----------------------------------------
# 5. Confidence status
# -----------------------------------------

def confidence_status(row):

    if row["inside_interval"]:
        return "Within Expected Range"

    if row["demand"] > row["upper_bound"]:
        return "Above Expected Range"

    return "Below Expected Range"


df["confidence_status"] = (
    df.apply(
        confidence_status,
        axis=1
    )
)


# -----------------------------------------
# 6. Coverage calculation
# -----------------------------------------

coverage = (
    df["inside_interval"].mean()
    * 100
)


outside_count = (
    (~df["inside_interval"]).sum()
)


# -----------------------------------------
# 7. Print summary
# -----------------------------------------

print(
    "\n========== FORECAST CONFIDENCE =========="
)

print(
    f"Observations: {len(df)}"
)

print(
    f"95% interval coverage: "
    f"{coverage:.2f}%"
)

print(
    f"Outside interval: "
    f"{outside_count}"
)


# -----------------------------------------
# 8. Confidence distribution
# -----------------------------------------

print(
    "\n========== CONFIDENCE STATUS =========="
)

print(
    df["confidence_status"]
    .value_counts()
)


# -----------------------------------------
# 9. Show observations outside interval
# -----------------------------------------

outside = df[
    ~df["inside_interval"]
].copy()


print(
    "\n========== OUTSIDE INTERVAL =========="
)


if len(outside) == 0:

    print(
        "All actual observations were "
        "within the forecast interval."
    )

else:

    print(
        outside[
            [
                "date",
                "demand",
                "forecast",
                "lower_bound",
                "upper_bound",
                "error",
                "interval_distance",
                "confidence_status"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )


# -----------------------------------------
# 10. Save confidence results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/confidence_analysis.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nConfidence analysis saved to: "
    f"{OUTPUT_PATH}"
)