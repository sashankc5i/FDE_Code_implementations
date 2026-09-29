from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data" / "generated"

PIPELINE_FILE = DATA_DIR / "sales_pipeline.parquet"
CUSTOMER_HEALTH_FILE = DATA_DIR / "customer_health.parquet"
PRICING_FILE = DATA_DIR / "pricing.parquet"


# ============================================================
# CONFIGURATION
# ============================================================

HIGH_SIGNAL_THRESHOLD = 20.0
MEDIUM_SIGNAL_THRESHOLD = 10.0


# ============================================================
# DATA LOADING
# ============================================================

def load_pipeline_data() -> pd.DataFrame:
    """Load sales pipeline data."""
    return pd.read_parquet(PIPELINE_FILE)


def load_customer_health() -> pd.DataFrame:
    """Load customer health data."""
    return pd.read_parquet(CUSTOMER_HEALTH_FILE)


def load_pricing_data() -> pd.DataFrame:
    """Load pricing data."""
    return pd.read_parquet(PRICING_FILE)


# ============================================================
# SIGNAL CLASSIFICATION
# ============================================================

def classify_signal(
    change_pct: float,
    direction: str,
) -> str:
    """
    Classify the magnitude of a driver change.

    For negative drivers:
        larger negative movement = stronger signal

    For positive drivers such as churn:
        larger positive movement = stronger signal.
    """

    magnitude = abs(change_pct)

    if magnitude >= HIGH_SIGNAL_THRESHOLD:
        return "HIGH"

    if magnitude >= MEDIUM_SIGNAL_THRESHOLD:
        return "MEDIUM"

    return "LOW"


# ============================================================
# PIPELINE ANALYSIS
# ============================================================

def analyze_pipeline(
    period: str,
    region: str,
    segment: str,
) -> dict:

    df = load_pipeline_data()

    target_period = pd.Timestamp(period)

    historical = df[
        (df["region"] == region)
        & (df["segment"] == segment)
        & (df["period"] < target_period)
    ]

    current = df[
        (df["region"] == region)
        & (df["segment"] == segment)
        & (df["period"] == target_period)
    ]

    if current.empty:
        return {
            "available": False,
            "reason": "No pipeline data found for investigation period.",
        }

    current_row = current.iloc[0]

    current_pipeline = float(
        current_row["pipeline_value"]
    )

    delayed_deals = int(
        current_row["delayed_deals"]
    )

    historical_average = float(
        historical["pipeline_value"].mean()
    ) if not historical.empty else None

    if historical_average and historical_average != 0:

        change_pct = (
            (
                current_pipeline
                - historical_average
            )
            / historical_average
        ) * 100

    else:
        change_pct = None

    signal = (
        classify_signal(change_pct, "negative")
        if change_pct is not None
        else "UNKNOWN"
    )

    return {
        "available": True,
        "current_pipeline": round(
            current_pipeline,
            2,
        ),
        "historical_average_pipeline": (
            round(historical_average, 2)
            if historical_average is not None
            else None
        ),
        "change_pct": (
            round(change_pct, 2)
            if change_pct is not None
            else None
        ),
        "delayed_deals": delayed_deals,
        "signal": signal,
    }


# ============================================================
# CUSTOMER HEALTH ANALYSIS
# ============================================================

def analyze_customer_health(
    period: str,
    region: str,
    segment: str,
) -> dict:

    df = load_customer_health()

    target_period = pd.Timestamp(period)

    historical = df[
        (df["region"] == region)
        & (df["segment"] == segment)
        & (df["period"] < target_period)
    ]

    current = df[
        (df["region"] == region)
        & (df["segment"] == segment)
        & (df["period"] == target_period)
    ]

    if current.empty:
        return {
            "available": False,
            "reason": (
                "No customer health data found "
                "for investigation period."
            ),
        }

    current_row = current.iloc[0]

    current_churn = float(
        current_row["churn_rate"]
    )

    churned_customers = int(
        current_row["churned_customers"]
    )

    historical_average = float(
        historical["churn_rate"].mean()
    ) if not historical.empty else None

    if (
        historical_average is not None
        and historical_average != 0
    ):

        change_pct = (
            (
                current_churn
                - historical_average
            )
            / historical_average
        ) * 100

    else:
        change_pct = None

    signal = (
        classify_signal(change_pct, "positive")
        if change_pct is not None
        else "UNKNOWN"
    )

    return {
        "available": True,
        "current_churn_rate": round(
            current_churn,
            4,
        ),
        "historical_average_churn_rate": (
            round(
                historical_average,
                4,
            )
            if historical_average is not None
            else None
        ),
        "change_pct": (
            round(change_pct, 2)
            if change_pct is not None
            else None
        ),
        "churned_customers": churned_customers,
        "signal": signal,
    }


# ============================================================
# PRICING ANALYSIS
# ============================================================

def analyze_pricing(
    period: str,
    region: str,
) -> dict:

    df = load_pricing_data()

    target_period = pd.Timestamp(period)

    historical = df[
        (df["region"] == region)
        & (df["period"] < target_period)
    ]

    current = df[
        (df["region"] == region)
        & (df["period"] == target_period)
    ]

    if current.empty:
        return {
            "available": False,
            "reason": "No pricing data found.",
        }

    current_average = float(
        current["price_index"].mean()
    )

    historical_average = float(
        historical["price_index"].mean()
    ) if not historical.empty else None

    if (
        historical_average is not None
        and historical_average != 0
    ):

        change_pct = (
            (
                current_average
                - historical_average
            )
            / historical_average
        ) * 100

    else:
        change_pct = None

    signal = (
        classify_signal(change_pct, "negative")
        if change_pct is not None
        else "UNKNOWN"
    )

    return {
        "available": True,
        "current_average_price_index": round(
            current_average,
            2,
        ),
        "historical_average_price_index": (
            round(
                historical_average,
                2,
            )
            if historical_average is not None
            else None
        ),
        "change_pct": (
            round(change_pct, 2)
            if change_pct is not None
            else None
        ),
        "signal": signal,
    }


# ============================================================
# COMPLETE DRIVER INVESTIGATION
# ============================================================

def investigate_drivers(
    period: str,
    region: str,
    segment: str,
) -> dict:
    """
    Investigate potential business drivers
    behind a forecast deviation.
    """

    pipeline = analyze_pipeline(
        period,
        region,
        segment,
    )

    customer_health = analyze_customer_health(
        period,
        region,
        segment,
    )

    pricing = analyze_pricing(
        period,
        region,
    )

    return {
        "investigation": {
            "period": period,
            "region": region,
            "segment": segment,
        },
        "drivers": {
            "pipeline": pipeline,
            "customer_health": customer_health,
            "pricing": pricing,
        },
    }


# ============================================================
# CLI
# ============================================================

def print_driver_report(
    result: dict,
) -> None:

    investigation = result["investigation"]
    drivers = result["drivers"]

    print(
        "\n"
        "====================================================\n"
        " DRIVER ANALYSIS\n"
        "===================================================="
    )

    print("\nINVESTIGATION")

    print(
        f"Period  : {investigation['period']}"
    )

    print(
        f"Region  : {investigation['region']}"
    )

    print(
        f"Segment : {investigation['segment']}"
    )

    print("\n--- PIPELINE ---")

    for key, value in drivers["pipeline"].items():
        print(f"{key}: {value}")

    print("\n--- CUSTOMER HEALTH ---")

    for key, value in drivers[
        "customer_health"
    ].items():
        print(f"{key}: {value}")

    print("\n--- PRICING ---")

    for key, value in drivers["pricing"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":

    result = investigate_drivers(
        period="2026-03-01",
        region="West",
        segment="Enterprise",
    )

    print_driver_report(result)