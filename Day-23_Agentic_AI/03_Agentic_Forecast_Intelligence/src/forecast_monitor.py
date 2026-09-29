from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = (
    BASE_DIR
    / "data"
    / "generated"
)

FORECAST_FILE = (
    DATA_DIR
    / "forecasts.parquet"
)


# ============================================================
# DATA LOADING
# ============================================================

def load_forecast_data() -> pd.DataFrame:
    """
    Load generated forecast and actual revenue data.
    """
    return pd.read_parquet(FORECAST_FILE)


# ============================================================
# VARIANCE CALCULATION
# ============================================================

def calculate_variance(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate absolute and percentage
    forecast variance.
    """

    result = df.copy()

    result["variance"] = (
        result["actual_revenue"]
        - result["forecast_revenue"]
    )

    result["variance_pct"] = (
        result["variance"]
        / result["forecast_revenue"]
    ) * 100

    return result


# ============================================================
# MATERIALITY DETECTION
# ============================================================

def detect_material_variance(
    df: pd.DataFrame,
    variance_threshold_pct: float = 10.0,
    variance_threshold_amount: float = 100_000,
) -> pd.DataFrame:
    """
    Identify revenue deviations that are
    significant enough to investigate.
    """

    result = df.copy()

    result["percentage_breach"] = (
        result["variance_pct"].abs()
        >= variance_threshold_pct
    )

    result["amount_breach"] = (
        result["variance"].abs()
        >= variance_threshold_amount
    )

    result["investigation_required"] = (
        result["percentage_breach"]
        & result["amount_breach"]
    )

    return result


# ============================================================
# MONITORING PIPELINE
# ============================================================

def monitor_forecast() -> pd.DataFrame:
    """
    Execute the complete forecast monitoring process.
    """

    df = load_forecast_data()

    df = calculate_variance(df)

    df = detect_material_variance(df)

    return df


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = monitor_forecast()

    investigations = result[
        result["investigation_required"]
    ].copy()

    investigations = investigations.sort_values(
        "variance_pct"
    )

    print(
        "\n"
        "====================================================\n"
        " FORECAST INVESTIGATION QUEUE\n"
        "====================================================\n"
    )

    if investigations.empty:

        print("No material forecast deviations detected.")

    else:

        print(
            investigations[
                [
                    "period",
                    "region",
                    "segment",
                    "forecast_revenue",
                    "actual_revenue",
                    "variance",
                    "variance_pct",
                ]
            ].to_string(index=False)
        )

    print(
        "\n"
        f"Total records monitored : {len(result)}"
    )

    print(
        "Investigation candidates : "
        f"{len(investigations)}"
    )