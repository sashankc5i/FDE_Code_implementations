import pandas as pd


# -----------------------------------------
# 1. Load business signals
# -----------------------------------------

SIGNAL_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/business_signals.csv"
)

signals = pd.read_csv(
    SIGNAL_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Load Topic 9 driver data
# -----------------------------------------

DRIVER_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

drivers = pd.read_csv(
    DRIVER_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 3. Select business driver columns
# -----------------------------------------

drivers = drivers[
    [
        "date",
        "price",
        "promotion",
        "holiday",
        "price_change",
        "price_change_pct",
        "promotion_intensity",
        "promotion_price_interaction"
    ]
]


# -----------------------------------------
# 4. Keep actionable signals
# -----------------------------------------

actionable = signals[
    signals["signal_priority"]
    .isin(
        [
            "Medium",
            "High"
        ]
    )
].copy()


# -----------------------------------------
# 5. Join driver context
# -----------------------------------------

actionable = actionable.merge(
    drivers,
    on="date",
    how="left"
)


# -----------------------------------------
# 6. Generate driver observations
# -----------------------------------------

def generate_driver_context(row):

    observations = []

    if row["promotion"] == 1:
        observations.append(
            "Promotion active"
        )

    if row["holiday"] == 1:
        observations.append(
            "Holiday indicator active"
        )

    if pd.notna(row["price_change_pct"]):

        if row["price_change_pct"] > 0:
            observations.append(
                f"Price increased "
                f"{row['price_change_pct']:.2f}%"
            )

        elif row["price_change_pct"] < 0:
            observations.append(
                f"Price decreased "
                f"{abs(row['price_change_pct']):.2f}%"
            )

    if not observations:
        observations.append(
            "No major driver flag identified "
            "from available features"
        )

    return "; ".join(
        observations
    )


actionable["driver_context"] = (
    actionable.apply(
        generate_driver_context,
        axis=1
    )
)


# -----------------------------------------
# 7. Print driver context
# -----------------------------------------

print(
    "\n========== DRIVER CONTEXT =========="
)

print(
    actionable[
        [
            "date",
            "signal_priority",
            "signal_score",
            "variance_pct",
            "severity",
            "is_anomaly",
            "confidence_status",
            "price",
            "promotion",
            "holiday",
            "price_change_pct",
            "driver_context"
        ]
    ]
    .sort_values(
        [
            "signal_score",
            "date"
        ],
        ascending=[
            False,
            True
        ]
    )
    .to_string(
        index=False
    )
)


# -----------------------------------------
# 8. Save driver context
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "outputs/driver_context.csv"
)

actionable.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nDriver context saved to: {OUTPUT_PATH}"
)