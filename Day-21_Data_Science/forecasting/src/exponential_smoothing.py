import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# -----------------------------------------
# 1. Load data
# -----------------------------------------

DATA_PATH = "forecasting/data/demand_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# -----------------------------------------
# 2. Split data
# -----------------------------------------

# Keep the final 20% as unseen test data

split_index = int(len(df) * 0.80)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()


# -----------------------------------------
# 3. Train Holt-Winters model
# -----------------------------------------

model = ExponentialSmoothing(
    train["demand"],
    trend="add",
    seasonal="add",
    seasonal_periods=7
)

fitted_model = model.fit(
    optimized=True
)


# -----------------------------------------
# 4. Generate forecast
# -----------------------------------------

forecast = fitted_model.forecast(
    len(test)
)


# -----------------------------------------
# 5. Store predictions
# -----------------------------------------

test["forecast"] = forecast.values


# -----------------------------------------
# 6. Calculate errors
# -----------------------------------------

test["error"] = (
    test["demand"]
    - test["forecast"]
)

test["absolute_error"] = (
    test["error"].abs()
)


# -----------------------------------------
# 7. Calculate metrics
# -----------------------------------------

mae = mean_absolute_error(
    test["demand"],
    test["forecast"]
)

rmse = np.sqrt(
    mean_squared_error(
        test["demand"],
        test["forecast"]
    )
)

mape = (
    test["absolute_error"]
    / test["demand"].replace(0, np.nan)
).mean() * 100

bias = test["error"].mean()


# -----------------------------------------
# 8. Print results
# -----------------------------------------

print("\n========== HOLT-WINTERS ==========")

print(f"Train rows: {len(train)}")
print(f"Test rows:  {len(test)}")

print(f"\nMAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Bias: {bias:.2f}")


# -----------------------------------------
# 9. Show sample forecasts
# -----------------------------------------

print("\n========== SAMPLE FORECASTS ==========")

print(
    test[
        [
            "date",
            "demand",
            "forecast",
            "error"
        ]
    ].head(10)
)