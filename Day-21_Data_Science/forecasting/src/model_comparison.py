import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

from statsmodels.tsa.holtwinters import ExponentialSmoothing


# -----------------------------------------
# 1. Load data
# -----------------------------------------

DATA_PATH = "forecasting/data/demand_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# -----------------------------------------
# 2. Helper function for metrics
# -----------------------------------------

def calculate_metrics(actual, forecast):

    error = actual - forecast

    mae = mean_absolute_error(
        actual,
        forecast
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            forecast
        )
    )

    mape = (
        error.abs()
        / actual.replace(0, np.nan)
    ).mean() * 100

    bias = error.mean()

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "Bias": bias
    }


# -----------------------------------------
# 3. Evaluate naive baseline
# -----------------------------------------

df["naive_forecast"] = (
    df["demand"].shift(1)
)

naive_eval = df.dropna(
    subset=["naive_forecast"]
)

naive_metrics = calculate_metrics(
    naive_eval["demand"],
    naive_eval["naive_forecast"]
)


# -----------------------------------------
# 4. Evaluate 7-day moving average
# -----------------------------------------

df["moving_average_forecast"] = (
    df["demand"]
    .rolling(7)
    .mean()
    .shift(1)
)

ma_eval = df.dropna(
    subset=["moving_average_forecast"]
)

ma_metrics = calculate_metrics(
    ma_eval["demand"],
    ma_eval["moving_average_forecast"]
)


# -----------------------------------------
# 5. Evaluate Holt-Winters
# -----------------------------------------

split_index = int(len(df) * 0.80)

train = df.iloc[:split_index]

test = df.iloc[split_index:].copy()


model = ExponentialSmoothing(
    train["demand"],
    trend="add",
    seasonal="add",
    seasonal_periods=7
)

fitted_model = model.fit(
    optimized=True
)

hw_forecast = fitted_model.forecast(
    len(test)
)

hw_metrics = calculate_metrics(
    test["demand"],
    pd.Series(
        hw_forecast.values,
        index=test.index
    )
)


# -----------------------------------------
# 6. Build comparison table
# -----------------------------------------

results = pd.DataFrame([
    {
        "Model": "Naive",
        **naive_metrics
    },
    {
        "Model": "7-Day Moving Average",
        **ma_metrics
    },
    {
        "Model": "Holt-Winters",
        **hw_metrics
    }
])


# -----------------------------------------
# 7. Sort by MAE
# -----------------------------------------

results = results.sort_values(
    "MAE"
).reset_index(drop=True)


# -----------------------------------------
# 8. Print comparison
# -----------------------------------------

print("\n========== FORECAST MODEL COMPARISON ==========")

print(
    results.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# -----------------------------------------
# 9. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "forecasting/"
    "outputs/model_comparison.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nComparison saved to: {OUTPUT_PATH}"
)