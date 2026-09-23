import pandas as pd


# -----------------------------------------
# 1. Load actual demand
# -----------------------------------------

ACTUAL_PATH = (
    "forecasting/"
    "data/demand_data.csv"
)

actual = pd.read_csv(
    ACTUAL_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 2. Load historical forecast
# -----------------------------------------

FORECAST_PATH = (
    "forecasting/"
    "outputs/forecast_with_intervals.csv"
)

forecast = pd.read_csv(
    FORECAST_PATH,
    parse_dates=["date"]
)


# -----------------------------------------
# 3. Inspect forecast columns
# -----------------------------------------

print(
    "\n========== FORECAST COLUMNS =========="
)

print(
    forecast.columns.tolist()
)


# -----------------------------------------
# 4. Prepare actual demand
# -----------------------------------------

actual = actual[
    [
        "date",
        "demand"
    ]
].copy()

actual = actual.rename(
    columns={
        "demand": "actual_demand"
    }
)


# -----------------------------------------
# 5. Inspect forecast structure
# -----------------------------------------

print(
    "\nHistorical forecast sample:"
)

print(
    forecast.head().to_string(
        index=False
    )
)


# -----------------------------------------
# 6. Prepare forecast
# -----------------------------------------

forecast = forecast[
    [
        "date",
        "forecast"
    ]
].copy()

forecast = forecast.rename(
    columns={
        "forecast": "forecast_demand"
    }
)


# -----------------------------------------
# 7. Combine actual and forecast
# -----------------------------------------

monitoring = actual.merge(
    forecast,
    on="date",
    how="inner"
)


# -----------------------------------------
# 8. Sort chronologically
# -----------------------------------------

monitoring = monitoring.sort_values(
    "date"
).reset_index(
    drop=True
)


# -----------------------------------------
# 9. Calculate error
# -----------------------------------------

monitoring["error"] = (
    monitoring["actual_demand"]
    - monitoring["forecast_demand"]
)


# -----------------------------------------
# 10. Calculate absolute error
# -----------------------------------------

monitoring["absolute_error"] = (
    monitoring["error"].abs()
)


# -----------------------------------------
# 11. Calculate variance percentage
# -----------------------------------------

monitoring["variance_pct"] = (
    monitoring["error"]
    / monitoring["forecast_demand"].replace(
        0,
        pd.NA
    )
) * 100


# -----------------------------------------
# 12. Save monitoring dataset
# -----------------------------------------

OUTPUT_PATH = (
    "topic-10-forecast-monitoring/"
    "data/monitoring_data.csv"
)

monitoring.to_csv(
    OUTPUT_PATH,
    index=False
)


# -----------------------------------------
# 13. Print summary
# -----------------------------------------

print(
    "\n========== MONITORING DATA =========="
)

print(
    f"Rows: {len(monitoring)}"
)

print(
    f"Actual rows: "
    f"{monitoring['actual_demand'].notna().sum()}"
)

print(
    f"Forecast rows: "
    f"{monitoring['forecast_demand'].notna().sum()}"
)

print(
    "\nFirst 10 rows:"
)

print(
    monitoring.head(10).to_string(
        index=False
    )
)

print(
    f"\nMonitoring data saved to: {OUTPUT_PATH}"
)