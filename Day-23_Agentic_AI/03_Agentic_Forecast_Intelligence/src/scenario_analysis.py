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
    return pd.read_parquet(
        FORECAST_FILE
    )


# ============================================================
# WHAT-IF ANALYSIS
# ============================================================

def run_pipeline_recovery_scenario(
    period: str,
    region: str,
    segment: str,
    recovery_pct: float,
    conversion_rate: float = 0.25,
) -> dict:
    """
    Estimate incremental revenue from recovering a
    percentage of the current pipeline.

    This is a scenario estimate, not a forecast model.
    """

    df = load_forecast_data()

    target_period = pd.Timestamp(period)

    forecast = df[
        (df["period"] == target_period)
        & (df["region"] == region)
        & (df["segment"] == segment)
    ]

    if forecast.empty:
        return {
            "available": False,
            "reason": "Forecast record not found.",
        }

    row = forecast.iloc[0]

    forecast_revenue = float(
        row["forecast_revenue"]
    )

    actual_revenue = float(
        row["actual_revenue"]
    )

    # --------------------------------------------------------
    # Current pipeline
    # --------------------------------------------------------

    pipeline_file = (
        DATA_DIR / "sales_pipeline.parquet"
    )

    pipeline_df = pd.read_parquet(
        pipeline_file
    )

    pipeline = pipeline_df[
        (pipeline_df["period"] == target_period)
        & (pipeline_df["region"] == region)
        & (pipeline_df["segment"] == segment)
    ]

    if pipeline.empty:
        return {
            "available": False,
            "reason": "Pipeline record not found.",
        }

    current_pipeline = float(
        pipeline.iloc[0]["pipeline_value"]
    )

    # --------------------------------------------------------
    # Scenario calculation
    # --------------------------------------------------------

    recovered_pipeline = (
        current_pipeline
        * recovery_pct
    )

    estimated_incremental_revenue = (
        recovered_pipeline
        * conversion_rate
    )

    scenario_revenue = (
        actual_revenue
        + estimated_incremental_revenue
    )

    remaining_gap = (
        forecast_revenue
        - scenario_revenue
    )

    gap_closed_pct = (
        estimated_incremental_revenue
        / (
            forecast_revenue
            - actual_revenue
        )
    ) * 100

    return {
        "available": True,
        "scenario": {
            "recovery_pct": recovery_pct,
            "conversion_rate": conversion_rate,
        },
        "baseline": {
            "forecast_revenue": round(
                forecast_revenue,
                2,
            ),
            "actual_revenue": round(
                actual_revenue,
                2,
            ),
            "current_pipeline": round(
                current_pipeline,
                2,
            ),
        },
        "scenario_result": {
            "recovered_pipeline": round(
                recovered_pipeline,
                2,
            ),
            "estimated_incremental_revenue": round(
                estimated_incremental_revenue,
                2,
            ),
            "scenario_revenue": round(
                scenario_revenue,
                2,
            ),
            "remaining_forecast_gap": round(
                remaining_gap,
                2,
            ),
            "gap_closed_pct": round(
                gap_closed_pct,
                2,
            ),
        },
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = run_pipeline_recovery_scenario(
        period="2026-03-01",
        region="West",
        segment="Enterprise",
        recovery_pct=0.25,
        conversion_rate=0.25,
    )

    print(
        "\n"
        "====================================================\n"
        " PIPELINE RECOVERY WHAT-IF ANALYSIS\n"
        "===================================================="
    )

    for key, value in result.items():
        print(f"\n{key}: {value}")