import pandas as pd


# -----------------------------------------
# 1. Load driver-context signals
# -----------------------------------------

DATA_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/driver_context.csv"
)

df = pd.read_csv(
    DATA_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Generate human-readable signal
# -----------------------------------------

def generate_signal(row):

    priority = row["signal_priority"]

    variance = row["variance_pct"]

    direction = (
        "above"
        if variance > 0
        else "below"
    )

    message = (
        f"{priority.upper()}: Demand is "
        f"{abs(variance):.2f}% {direction} forecast."
    )

    if row["is_anomaly"]:
        message += (
            " The deviation is statistically unusual."
        )

    if not row["inside_interval"]:
        message += (
            " Actual demand is outside the "
            "95% forecast interval."
        )

    if row["persistent_deviation"]:
        message += (
            " The deviation is persistent."
        )

    if row["driver_context"]:
        message += (
            f" Driver context: "
            f"{row['driver_context']}."
        )

    return message


df["signal_message"] = (
    df.apply(
        generate_signal,
        axis=1
    )
)


# -----------------------------------------
# 3. Recommended action
# -----------------------------------------

def recommended_action(row):

    if row["signal_priority"] == "High":

        return (
            "Investigate immediately. "
            "Validate actual data quality, review "
            "forecast generation, and investigate "
            "relevant business drivers."
        )

    elif row["signal_priority"] == "Medium":

        return (
            "Investigate if the deviation continues "
            "or additional evidence emerges."
        )

    elif row["signal_priority"] == "Low":

        return (
            "Continue monitoring."
        )

    return (
        "No immediate action."
    )


df["recommended_action"] = (
    df.apply(
        recommended_action,
        axis=1
    )
)


# -----------------------------------------
# 4. Select report columns
# -----------------------------------------

report = df[
    [
        "date",
        "signal_priority",
        "signal_score",
        "actual_demand",
        "forecast_demand",
        "variance_pct",
        "severity",
        "is_anomaly",
        "persistent_deviation",
        "confidence_status",
        "driver_context",
        "signal_message",
        "recommended_action"
    ]
].copy()


# -----------------------------------------
# 5. Sort by priority
# -----------------------------------------

priority_order = {
    "High": 0,
    "Medium": 1,
    "Low": 2
}

report["priority_order"] = (
    report["signal_priority"]
    .map(priority_order)
)


report = report.sort_values(
    [
        "priority_order",
        "date"
    ]
).drop(
    columns=["priority_order"]
)


# -----------------------------------------
# 6. Print high-priority signals
# -----------------------------------------

print(
    "\n========== FINAL BUSINESS SIGNAL REPORT =========="
)

high_priority = report[
    report["signal_priority"]
    == "High"
]


for _, row in high_priority.iterrows():

    print(
        f"\nDate: {row['date'].date()}"
    )

    print(
        f"Priority: {row['signal_priority']}"
    )

    print(
        f"Score: {row['signal_score']}"
    )

    print(
        f"Actual: {row['actual_demand']:.2f}"
    )

    print(
        f"Forecast: {row['forecast_demand']:.2f}"
    )

    print(
        f"Variance: {row['variance_pct']:.2f}%"
    )

    print(
        f"Driver context: "
        f"{row['driver_context']}"
    )

    print(
        f"Signal: "
        f"{row['signal_message']}"
    )

    print(
        f"Action: "
        f"{row['recommended_action']}"
    )


# -----------------------------------------
# 7. Save final report
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/final_signal_report.csv"
)

report.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nFinal signal report saved to: {OUTPUT_PATH}"
)