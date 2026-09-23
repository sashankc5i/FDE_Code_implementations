import pandas as pd


# -----------------------------------------
# 1. Load anomaly data
# -----------------------------------------

DATA_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/anomaly_detection.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Configuration
# -----------------------------------------

VARIANCE_THRESHOLD = 10
PERSISTENCE_THRESHOLD = 3


# -----------------------------------------
# 3. Determine meaningful deviation
# -----------------------------------------

df["meaningful_deviation"] = (
    df["absolute_variance_pct"]
    >= VARIANCE_THRESHOLD
)


# -----------------------------------------
# 4. Determine deviation direction
# -----------------------------------------

def deviation_direction(row):

    if not row["meaningful_deviation"]:
        return "Normal"

    if row["error"] > 0:
        return "Above Forecast"

    elif row["error"] < 0:
        return "Below Forecast"

    return "Normal"


df["deviation_direction"] = (
    df.apply(
        deviation_direction,
        axis=1
    )
)


# -----------------------------------------
# 5. Track consecutive direction
# -----------------------------------------

streak_id = (
    (
        df["deviation_direction"]
        != df["deviation_direction"].shift()
    )
    .cumsum()
)


df["streak_id"] = streak_id


df["streak_length"] = (
    df.groupby(
        "streak_id"
    )
    .cumcount()
    + 1
)


# -----------------------------------------
# 6. Identify persistent deviations
# -----------------------------------------

df["persistent_deviation"] = (
    (
        df["streak_length"]
        >= PERSISTENCE_THRESHOLD
    )
    &
    (
        df["deviation_direction"]
        != "Normal"
    )
)


# -----------------------------------------
# 7. Print summary
# -----------------------------------------

print(
    "\n========== PERSISTENCE DETECTION =========="
)

print(
    f"Variance threshold: "
    f"{VARIANCE_THRESHOLD}%"
)

print(
    f"Persistence threshold: "
    f"{PERSISTENCE_THRESHOLD} consecutive observations"
)


persistent = df[
    df["persistent_deviation"]
].copy()


print(
    f"\nPersistent observations: "
    f"{len(persistent)}"
)


# -----------------------------------------
# 8. Display persistent deviations
# -----------------------------------------

if len(persistent) == 0:

    print(
        "\nNo persistent deviations detected."
    )

else:

    print(
        "\n========== PERSISTENT DEVIATIONS =========="
    )

    print(
        persistent[
            [
                "date",
                "actual_demand",
                "forecast_demand",
                "error",
                "variance_pct",
                "deviation_direction",
                "streak_length"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}"
        )
    )


# -----------------------------------------
# 9. Save output
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/persistence_detection.csv"
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nPersistence analysis saved to: "
    f"{OUTPUT_PATH}"
)