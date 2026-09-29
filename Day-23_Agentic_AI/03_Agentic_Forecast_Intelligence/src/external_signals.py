from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "generated"

EXTERNAL_SIGNAL_FILE = (
    DATA_DIR / "external_signals.parquet"
)


# ============================================================
# DATA LOADING
# ============================================================

def load_external_signals() -> pd.DataFrame:
    """Load generated external market signals."""

    return pd.read_parquet(
        EXTERNAL_SIGNAL_FILE
    )


# ============================================================
# SIGNAL CLASSIFICATION
# ============================================================

def classify_demand_signal(
    change_pct: float,
) -> str:
    """
    Classify the change in external demand
    relative to the historical baseline.
    """

    if change_pct <= -10:
        return "HIGH"

    if change_pct <= -5:
        return "MEDIUM"

    return "LOW"


# ============================================================
# EXTERNAL SIGNAL ANALYSIS
# ============================================================

def analyze_external_signals(
    period: str,
    region: str,
) -> dict:
    """
    Compare the current external demand signal
    with the historical regional baseline.
    """

    df = load_external_signals()

    target_period = pd.Timestamp(period)

    # --------------------------------------------------------
    # Filter region
    # --------------------------------------------------------

    region_data = df[
        df["region"] == region
    ].copy()

    if region_data.empty:
        return {
            "available": False,
            "reason": (
                f"No external signal data found "
                f"for region {region}."
            ),
        }

    # --------------------------------------------------------
    # Current signal
    # --------------------------------------------------------

    current = region_data[
        region_data["period"] == target_period
    ]

    if current.empty:
        return {
            "available": False,
            "reason": (
                f"No external signal found for "
                f"{region} in {period}."
            ),
        }

    current_row = current.iloc[0]

    current_demand = float(
        current_row["demand_index"]
    )

    current_signal = str(
        current_row["signal"]
    )

    # --------------------------------------------------------
    # Historical baseline
    # --------------------------------------------------------

    historical = region_data[
        region_data["period"] < target_period
    ]

    if historical.empty:
        return {
            "available": False,
            "reason": (
                "No historical baseline available."
            ),
        }

    historical_average = float(
        historical["demand_index"].mean()
    )

    # --------------------------------------------------------
    # Change from historical baseline
    # --------------------------------------------------------

    change_pct = (
        (
            current_demand
            - historical_average
        )
        / historical_average
    ) * 100

    signal_strength = classify_demand_signal(
        change_pct
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {
        "available": True,
        "period": period,
        "region": region,
        "current_demand_index": round(
            current_demand,
            2,
        ),
        "historical_average_demand_index": round(
            historical_average,
            2,
        ),
        "change_pct": round(
            change_pct,
            2,
        ),
        "market_signal": current_signal,
        "signal_strength": signal_strength,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = analyze_external_signals(
        period="2026-03-01",
        region="West",
    )

    print(
        "\n"
        "====================================================\n"
        " EXTERNAL SIGNAL ANALYSIS\n"
        "===================================================="
    )

    for key, value in result.items():
        print(f"{key}: {value}")