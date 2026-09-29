from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "generated"

FORECAST_FILE = DATA_DIR / "forecasts.parquet"


# ============================================================
# DATA LOADING
# ============================================================

def load_forecast_data() -> pd.DataFrame:
    """Load forecast and actual revenue data."""
    return pd.read_parquet(FORECAST_FILE)


# ============================================================
# TREND ANALYSIS
# ============================================================

def analyze_revenue_trend(
    region: str,
    segment: str,
    period: str,
) -> dict:
    """
    Analyze the historical revenue variance trend
    for a specific region and segment.
    """

    df = load_forecast_data()

    target_period = pd.Timestamp(period)

    history = df[
        (df["region"] == region)
        & (df["segment"] == segment)
        & (df["period"] <= target_period)
    ].copy()

    history["variance"] = (
        history["actual_revenue"]
        - history["forecast_revenue"]
    )

    history["variance_pct"] = (
        history["variance"]
        / history["forecast_revenue"]
    ) * 100

    history = history.sort_values("period")

    if history.empty:
        return {
            "available": False,
            "reason": "No historical data available.",
        }

    variance_values = (
        history["variance_pct"]
        .round(2)
        .tolist()
    )

    current_variance = float(
        history.iloc[-1]["variance_pct"]
    )

    # --------------------------------------------------------
    # Persistence
    # --------------------------------------------------------

    negative_periods = (
        history["variance_pct"] < 0
    ).sum()

    # Consecutive negative periods
    consecutive_negative = 0

    for value in reversed(
        history["variance_pct"].tolist()
    ):
        if value < 0:
            consecutive_negative += 1
        else:
            break

    # --------------------------------------------------------
    # Direction
    # --------------------------------------------------------

    direction = "STABLE"

    if len(history) >= 2:

        previous = float(
            history.iloc[-2]["variance_pct"]
        )

        if current_variance < previous:
            direction = "DETERIORATING"

        elif current_variance > previous:
            direction = "IMPROVING"

    # --------------------------------------------------------
    # Acceleration
    # --------------------------------------------------------

    acceleration = False

    if len(history) >= 3:

        previous = float(
            history.iloc[-2]["variance_pct"]
        )

        two_periods_ago = float(
            history.iloc[-3]["variance_pct"]
        )

        previous_change = (
            previous - two_periods_ago
        )

        current_change = (
            current_variance - previous
        )

        if (
            current_change < 0
            and current_change < previous_change
        ):
            acceleration = True

    # --------------------------------------------------------
    # Trend classification
    # --------------------------------------------------------

    if (
        consecutive_negative >= 2
        and direction == "DETERIORATING"
    ):
        trend = "PERSISTENT_DETERIORATION"

    elif direction == "DETERIORATING":
        trend = "DETERIORATING"

    elif direction == "IMPROVING":
        trend = "IMPROVING"

    else:
        trend = "STABLE"

    return {
        "available": True,
        "history": variance_values,
        "current_variance_pct": round(
            current_variance,
            2,
        ),
        "negative_periods": int(
            negative_periods
        ),
        "consecutive_negative_periods": int(
            consecutive_negative
        ),
        "direction": direction,
        "acceleration": acceleration,
        "trend": trend,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = analyze_revenue_trend(
        region="West",
        segment="Enterprise",
        period="2026-03-01",
    )

    print(
        "\n"
        "====================================================\n"
        " REVENUE TREND ANALYSIS\n"
        "===================================================="
    )

    for key, value in result.items():
        print(f"{key}: {value}")