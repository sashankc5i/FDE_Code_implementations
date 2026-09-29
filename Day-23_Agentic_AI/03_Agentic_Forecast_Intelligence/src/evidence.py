from datetime import datetime, timezone
from pathlib import Path

from src.driver_analysis import investigate_drivers
from src.external_signals import analyze_external_signals
from src.forecast_monitor import monitor_forecast
from src.trend_analysis import analyze_revenue_trend


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = (
    BASE_DIR
    / "data"
    / "generated"
)


# ============================================================
# EVIDENCE BUILDER
# ============================================================

def build_forecast_evidence(
    period: str,
    region: str,
    segment: str,
) -> dict:
    """
    Consolidate deterministic investigation outputs into
    traceable evidence items.

    Evidence is factual output from the analytical layer.
    It does not contain LLM-generated conclusions.
    """

    evidence = []

    # --------------------------------------------------------
    # Forecast variance
    # --------------------------------------------------------

    forecast_df = monitor_forecast()

    forecast_match = forecast_df[
        (forecast_df["period"] == period)
        & (forecast_df["region"] == region)
        & (forecast_df["segment"] == segment)
    ]

    if not forecast_match.empty:

        row = forecast_match.iloc[0]

        variance_pct = float(
            row["variance_pct"]
        )

        variance = float(
            row["variance"]
        )

        if abs(variance_pct) >= 10:

            evidence.append(
                {
                    "evidence_id": "EV001",
                    "type": "FORECAST_VARIANCE",
                    "signal": "revenue_deterioration"
                    if variance_pct < 0
                    else "revenue_improvement",
                    "period": period,
                    "region": region,
                    "segment": segment,
                    "value": variance_pct,
                    "unit": "percent",
                    "severity": "HIGH",
                    "description": (
                        f"Revenue variance is "
                        f"{variance_pct:.2f}% "
                        f"({variance:,.2f} absolute variance)."
                    ),
                }
            )

    # --------------------------------------------------------
    # Driver analysis
    # --------------------------------------------------------

    drivers = investigate_drivers(
        period=period,
        region=region,
        segment=segment,
    )

    # --------------------------------------------------------
    # Pipeline
    # --------------------------------------------------------

    pipeline = drivers.get(
        "pipeline",
        {}
    )

    if pipeline:

        change_pct = pipeline.get(
            "change_pct"
        )

        if (
            change_pct is not None
            and float(change_pct) <= -20
        ):

            evidence.append(
                {
                    "evidence_id": "EV002",
                    "type": "PIPELINE",
                    "signal": "pipeline_deterioration",
                    "period": period,
                    "region": region,
                    "segment": segment,
                    "value": float(
                        change_pct
                    ),
                    "unit": "percent",
                    "severity": "HIGH",
                    "description": (
                        f"Sales pipeline declined "
                        f"{abs(float(change_pct)):.2f}% "
                        f"versus the historical baseline."
                    ),
                }
            )

    # --------------------------------------------------------
    # Customer health
    # --------------------------------------------------------

    customer_health = drivers.get(
        "customer_health",
        {}
    )

    if customer_health:

        change_pct = customer_health.get(
            "change_pct"
        )

        if (
            change_pct is not None
            and float(change_pct) >= 20
        ):

            evidence.append(
                {
                    "evidence_id": "EV003",
                    "type": "CUSTOMER_HEALTH",
                    "signal": "customer_churn",
                    "period": period,
                    "region": region,
                    "segment": segment,
                    "value": float(
                        change_pct
                    ),
                    "unit": "percent",
                    "severity": "HIGH",
                    "description": (
                        f"Customer churn increased "
                        f"{float(change_pct):.2f}% "
                        f"versus the historical baseline."
                    ),
                }
            )

    # --------------------------------------------------------
    # Pricing
    # --------------------------------------------------------

    pricing = drivers.get(
        "pricing",
        {}
    )

    if pricing:

        change_pct = pricing.get(
            "change_pct"
        )

        if change_pct is not None:

            pricing_change = float(
                change_pct
            )

            if abs(pricing_change) >= 10:

                severity = "MEDIUM"

            else:

                severity = "LOW"

            evidence.append(
                {
                    "evidence_id": "EV004",
                    "type": "PRICING",
                    "signal": "pricing",
                    "period": period,
                    "region": region,
                    "segment": segment,
                    "value": pricing_change,
                    "unit": "percent",
                    "severity": severity,
                    "description": (
                        f"Average price index changed "
                        f"{pricing_change:.2f}% "
                        f"versus the historical baseline."
                    ),
                }
            )

    # --------------------------------------------------------
    # Revenue trend
    # --------------------------------------------------------

    trend = analyze_revenue_trend(
        period=period,
        region=region,
        segment=segment,
    )

    if trend.get(
        "trend"
    ) == "PERSISTENT_DETERIORATION":

        evidence.append(
            {
                "evidence_id": "EV005",
                "type": "REVENUE_TREND",
                "signal": "revenue_deterioration",
                "period": period,
                "region": region,
                "segment": segment,
                "value": trend.get(
                    "current_variance_pct"
                ),
                "unit": "percent",
                "severity": "HIGH",
                "description": (
                    "Revenue variance shows "
                    f"{trend.get('consecutive_negative_periods', 0)} "
                    "consecutive negative periods "
                    "with persistent deterioration."
                ),
            }
        )

    # --------------------------------------------------------
    # External demand
    # --------------------------------------------------------

    market = analyze_external_signals(
        period=period,
        region=region,
    )

    if market.get(
        "available"
    ):

        change_pct = market.get(
            "change_pct"
        )

        if (
            change_pct is not None
            and float(change_pct) <= -5
        ):

            evidence.append(
                {
                    "evidence_id": "EV006",
                    "type": "EXTERNAL_DEMAND",
                    "signal": "external_demand",
                    "period": period,
                    "region": region,
                    "segment": segment,
                    "value": float(
                        change_pct
                    ),
                    "unit": "percent",
                    "severity": (
                        "HIGH"
                        if float(change_pct) <= -10
                        else "MEDIUM"
                    ),
                    "description": (
                        f"Regional demand index declined "
                        f"{abs(float(change_pct)):.2f}% "
                        f"versus the historical baseline."
                    ),
                }
            )

    # --------------------------------------------------------
    # Return evidence package
    # --------------------------------------------------------

    return {
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "period": period,

        "region": region,

        "segment": segment,

        "evidence": evidence,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = build_forecast_evidence(
        period="2026-03-01",
        region="West",
        segment="Enterprise",
    )

    print(
        "\n"
        "====================================================\n"
        " FORECAST EVIDENCE\n"
        "===================================================="
    )

    for item in result["evidence"]:

        print(
            f"\n{item['evidence_id']}"
        )

        print(
            f"Signal   : {item['signal']}"
        )

        print(
            f"Severity : {item['severity']}"
        )

        print(
            f"Value    : {item['value']} "
            f"{item['unit']}"
        )

        print(
            f"Evidence : {item['description']}"
        )