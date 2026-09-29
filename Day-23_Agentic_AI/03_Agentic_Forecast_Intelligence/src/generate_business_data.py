from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

SEED = 42

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_DIR = (
    BASE_DIR
    / "data"
    / "generated"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

rng = np.random.default_rng(SEED)


# ============================================================
# BUSINESS DIMENSIONS
# ============================================================

REGIONS = [
    "North",
    "South",
    "East",
    "West",
]

SEGMENTS = [
    "Enterprise",
    "Mid-Market",
    "SMB",
]

PRODUCTS = [
    "Analytics Platform",
    "Data Platform",
    "Cloud Services",
    "AI Solutions",
    "Managed Services",
]


# ============================================================
# TIME
# ============================================================

PERIODS = pd.date_range(
    start="2025-04-01",
    end="2026-03-01",
    freq="MS",
)


# ============================================================
# CUSTOMER MASTER
# ============================================================

def generate_customers() -> pd.DataFrame:

    rows = []

    customer_id = 1

    for region in REGIONS:

        for segment in SEGMENTS:

            if segment == "Enterprise":
                customer_count = 80

            elif segment == "Mid-Market":
                customer_count = 150

            else:
                customer_count = 300

            for _ in range(customer_count):

                rows.append(
                    {
                        "customer_id": f"CUST{customer_id:05d}",
                        "region": region,
                        "segment": segment,
                        "product": rng.choice(PRODUCTS),
                        "annual_contract_value": round(
                            {
                                "Enterprise": rng.uniform(
                                    150_000,
                                    500_000,
                                ),
                                "Mid-Market": rng.uniform(
                                    50_000,
                                    150_000,
                                ),
                                "SMB": rng.uniform(
                                    10_000,
                                    50_000,
                                ),
                            }[segment],
                            2,
                        ),
                    }
                )

                customer_id += 1

    return pd.DataFrame(rows)


# ============================================================
# FORECAST + ACTUAL REVENUE
# ============================================================

def generate_forecasts(
    customers: pd.DataFrame,
) -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        month_index = (
            period.year * 12
            + period.month
        )

        for region in REGIONS:

            for segment in SEGMENTS:

                segment_customers = customers[
                    (customers["region"] == region)
                    & (customers["segment"] == segment)
                ]

                base_revenue = (
                    segment_customers[
                        "annual_contract_value"
                    ].sum()
                    / 12
                )

                growth_factor = (
                    1
                    + 0.015
                    * (
                        period.month
                        - 1
                    )
                )

                forecast = (
                    base_revenue
                    * growth_factor
                )

                # Normal business noise
                actual_factor = rng.normal(
                    1.0,
                    0.025,
                )

                # ------------------------------------------------
                # INTENTIONAL BUSINESS SHOCK
                # ------------------------------------------------
                #
                # West + Enterprise deteriorates in 2026-01
                # and becomes worse over the next two months.
                #
                if (
                    region == "West"
                    and segment == "Enterprise"
                    and period >= pd.Timestamp("2026-01-01")
                ):
                    months_since_shock = (
                        period.month - 1
                    )

                    actual_factor -= (
                        0.08
                        + 0.035
                        * months_since_shock
                    )

                actual = (
                    forecast
                    * actual_factor
                )

                rows.append(
                    {
                        "period": period,
                        "region": region,
                        "segment": segment,
                        "forecast_revenue": round(
                            forecast,
                            2,
                        ),
                        "actual_revenue": round(
                            actual,
                            2,
                        ),
                    }
                )

    return pd.DataFrame(rows)


# ============================================================
# SALES PIPELINE
# ============================================================

def generate_pipeline() -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        for region in REGIONS:

            for segment in SEGMENTS:

                pipeline = rng.uniform(
                    500_000,
                    3_000_000,
                )

                delayed_deals = rng.poisson(
                    1
                )

                # West Enterprise deterioration
                if (
                    region == "West"
                    and segment == "Enterprise"
                    and period >= pd.Timestamp("2026-01-01")
                ):
                    pipeline *= 0.82
                    delayed_deals += rng.integers(
                        2,
                        5,
                    )

                rows.append(
                    {
                        "period": period,
                        "region": region,
                        "segment": segment,
                        "pipeline_value": round(
                            pipeline,
                            2,
                        ),
                        "delayed_deals": int(
                            delayed_deals
                        ),
                    }
                )

    return pd.DataFrame(rows)


# ============================================================
# CUSTOMER HEALTH
# ============================================================

def generate_customer_health(
    customers: pd.DataFrame,
) -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        for region in REGIONS:

            for segment in SEGMENTS:

                group = customers[
                    (customers["region"] == region)
                    & (customers["segment"] == segment)
                ]

                customer_count = len(group)

                churn_rate = rng.uniform(
                    0.015,
                    0.05,
                )

                # West Enterprise deterioration
                if (
                    region == "West"
                    and segment == "Enterprise"
                    and period >= pd.Timestamp("2026-01-01")
                ):
                    churn_rate += 0.06

                churned = max(
                    1,
                    int(
                        customer_count
                        * churn_rate
                    ),
                )

                rows.append(
                    {
                        "period": period,
                        "region": region,
                        "segment": segment,
                        "active_customers": (
                            customer_count
                        ),
                        "churned_customers": churned,
                        "churn_rate": round(
                            churned
                            / customer_count,
                            4,
                        ),
                    }
                )

    return pd.DataFrame(rows)


# ============================================================
# PRICING
# ============================================================

def generate_pricing() -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        for region in REGIONS:

            for product in PRODUCTS:

                price_index = rng.normal(
                    100,
                    3,
                )

                rows.append(
                    {
                        "period": period,
                        "region": region,
                        "product": product,
                        "price_index": round(
                            price_index,
                            2,
                        ),
                    }
                )

    return pd.DataFrame(rows)


# ============================================================
# MARKETING
# ============================================================

def generate_marketing() -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        for region in REGIONS:

            spend = rng.uniform(
                100_000,
                500_000,
            )

            leads = int(
                spend
                * rng.uniform(
                    0.002,
                    0.004,
                )
            )

            rows.append(
                {
                    "period": period,
                    "region": region,
                    "marketing_spend": round(
                        spend,
                        2,
                    ),
                    "qualified_leads": leads,
                }
            )

    return pd.DataFrame(rows)


# ============================================================
# EXTERNAL SIGNALS
# ============================================================

def generate_external_signals() -> pd.DataFrame:

    rows = []

    for period in PERIODS:

        for region in REGIONS:

            demand_index = rng.normal(
                100,
                3,
            )

            signal = (
                "Stable market demand"
            )

            # External signal corresponding
            # to the West deterioration.
            if (
                region == "West"
                and period >= pd.Timestamp("2026-01-01")
            ):
                demand_index -= 7

                signal = (
                    "Regional enterprise demand "
                    "showing signs of contraction"
                )

            rows.append(
                {
                    "period": period,
                    "region": region,
                    "demand_index": round(
                        demand_index,
                        2,
                    ),
                    "signal": signal,
                }
            )

    return pd.DataFrame(rows)


# ============================================================
# MAIN
# ============================================================

def main():

    print("Generating synthetic business data...")

    customers = generate_customers()

    forecasts = generate_forecasts(
        customers
    )

    pipeline = generate_pipeline()

    customer_health = (
        generate_customer_health(
            customers
        )
    )

    pricing = generate_pricing()

    marketing = generate_marketing()

    external_signals = (
        generate_external_signals()
    )

    customers.to_parquet(
        OUTPUT_DIR / "customers.parquet",
        index=False,
    )

    forecasts.to_parquet(
        OUTPUT_DIR / "forecasts.parquet",
        index=False,
    )

    pipeline.to_parquet(
        OUTPUT_DIR / "sales_pipeline.parquet",
        index=False,
    )

    customer_health.to_parquet(
        OUTPUT_DIR / "customer_health.parquet",
        index=False,
    )

    pricing.to_parquet(
        OUTPUT_DIR / "pricing.parquet",
        index=False,
    )

    marketing.to_parquet(
        OUTPUT_DIR / "marketing.parquet",
        index=False,
    )

    external_signals.to_parquet(
        OUTPUT_DIR / "external_signals.parquet",
        index=False,
    )

    print("\nGeneration complete.\n")

    print(
        f"Customers: "
        f"{len(customers):,}"
    )

    print(
        f"Forecast records: "
        f"{len(forecasts):,}"
    )

    print(
        f"Pipeline records: "
        f"{len(pipeline):,}"
    )

    print(
        f"Customer health records: "
        f"{len(customer_health):,}"
    )

    print(
        f"\nOutput directory:\n"
        f"{OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()