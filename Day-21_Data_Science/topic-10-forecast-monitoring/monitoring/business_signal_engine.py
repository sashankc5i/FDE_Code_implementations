import pandas as pd


# -----------------------------------------
# 1. Load monitoring outputs
# -----------------------------------------

VARIANCE_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/variance_analysis.csv"
)

ANOMALY_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/anomaly_detection.csv"
)

PERSISTENCE_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/persistence_detection.csv"
)

CONFIDENCE_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/confidence_analysis.csv"
)


variance = pd.read_csv(
    VARIANCE_PATH,
    parse_dates=["date"]
)

anomaly = pd.read_csv(
    ANOMALY_PATH,
    parse_dates=["date"]
)

persistence = pd.read_csv(
    PERSISTENCE_PATH,
    parse_dates=["date"]
)

confidence = pd.read_csv(
    CONFIDENCE_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Select required columns
# -----------------------------------------

variance = variance[
    [
        "date",
        "actual_demand",
        "forecast_demand",
        "error",
        "absolute_error",
        "variance_pct",
        "absolute_variance_pct",
        "severity",
        "direction"
    ]
]


anomaly = anomaly[
    [
        "date",
        "error_zscore",
        "is_anomaly",
        "anomaly_type"
    ]
]


persistence = persistence[
    [
        "date",
        "streak_length",
        "persistent_deviation"
    ]
]


confidence = confidence[
    [
        "date",
        "inside_interval",
        "confidence_status",
        "interval_distance"
    ]
]


# -----------------------------------------
# 3. Merge monitoring signals
# -----------------------------------------

signals = variance.merge(
    anomaly,
    on="date",
    how="left"
)

signals = signals.merge(
    persistence,
    on="date",
    how="left"
)

signals = signals.merge(
    confidence,
    on="date",
    how="left"
)


# -----------------------------------------
# 4. Calculate signal score
# -----------------------------------------

def calculate_score(row):

    score = 0

    # Severity contribution
    severity_scores = {
        "Normal": 0,
        "Watch": 1,
        "Warning": 2,
        "Critical": 3
    }

    score += severity_scores.get(
        row["severity"],
        0
    )

    # Anomaly contribution
    if row["is_anomaly"]:
        score += 2

    # Persistence contribution
    if row["persistent_deviation"]:
        score += 3

    # Confidence contribution
    if not row["inside_interval"]:
        score += 2

    return score


signals["signal_score"] = (
    signals.apply(
        calculate_score,
        axis=1
    )
)


# -----------------------------------------
# 5. Assign signal priority
# -----------------------------------------

def assign_priority(score):

    if score >= 6:
        return "High"

    elif score >= 3:
        return "Medium"

    elif score >= 1:
        return "Low"

    return "None"


signals["signal_priority"] = (
    signals["signal_score"]
    .apply(assign_priority)
)


# -----------------------------------------
# 6. Generate business action
# -----------------------------------------

def generate_action(row):

    if row["signal_priority"] == "High":

        return (
            "Investigate immediately: "
            "multiple monitoring signals indicate "
            "meaningful deviation."
        )

    elif row["signal_priority"] == "Medium":

        return (
            "Investigate forecast deviation "
            "and review relevant business drivers."
        )

    elif row["signal_priority"] == "Low":

        return (
            "Monitor deviation for persistence "
            "or additional evidence."
        )

    return "No immediate action required."


signals["recommended_action"] = (
    signals.apply(
        generate_action,
        axis=1
    )
)


# -----------------------------------------
# 7. Generate signal explanation
# -----------------------------------------

def generate_explanation(row):

    reasons = []

    if row["severity"] != "Normal":
        reasons.append(
            f"variance={row['variance_pct']:.2f}%"
        )

    if row["is_anomaly"]:
        reasons.append(
            f"anomaly_z={row['error_zscore']:.2f}"
        )

    if row["persistent_deviation"]:
        reasons.append(
            f"persistent_streak={int(row['streak_length'])}"
        )

    if not row["inside_interval"]:
        reasons.append(
            "outside forecast interval"
        )

    if not reasons:
        return "Forecast behavior within expected range."

    return "; ".join(reasons)


signals["signal_explanation"] = (
    signals.apply(
        generate_explanation,
        axis=1
    )
)


# -----------------------------------------
# 8. Print summary
# -----------------------------------------

print(
    "\n========== BUSINESS SIGNAL ENGINE =========="
)

print(
    f"Total observations: {len(signals)}"
)


print(
    "\n========== PRIORITY DISTRIBUTION =========="
)

print(
    signals[
        "signal_priority"
    ].value_counts()
)


# -----------------------------------------
# 9. Display actionable signals
# -----------------------------------------

actionable = signals[
    signals["signal_priority"]
    != "None"
].copy()


print(
    "\n========== ACTIONABLE SIGNALS =========="
)


if len(actionable) == 0:

    print(
        "No actionable signals detected."
    )

else:

    print(
        actionable[
            [
                "date",
                "actual_demand",
                "forecast_demand",
                "variance_pct",
                "severity",
                "is_anomaly",
                "persistent_deviation",
                "inside_interval",
                "signal_score",
                "signal_priority",
                "signal_explanation"
            ]
        ]
        .sort_values(
            "signal_score",
            ascending=False
        )
        .to_string(
            index=False
        )
    )


# -----------------------------------------
# 10. Save business signals
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/business_signals.csv"
)

signals.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nBusiness signals saved to: "
    f"{OUTPUT_PATH}"
)