import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error


# -----------------------------------------
# 1. Load data
# -----------------------------------------

DATA_PATH = "forecasting/data/demand_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# -----------------------------------------
# 2. Create naive forecast
# -----------------------------------------

# Naive forecast:
# Today's forecast = yesterday's actual demand

df["forecast"] = df["demand"].shift(1)


# Remove first row because it has no previous-day value
evaluation_df = df.dropna(
    subset=["forecast"]
).copy()


# -----------------------------------------
# 3. Calculate forecast errors
# -----------------------------------------

evaluation_df["error"] = (
    evaluation_df["demand"]
    - evaluation_df["forecast"]
)

evaluation_df["absolute_error"] = (
    evaluation_df["error"].abs()
)


# -----------------------------------------
# 4. Calculate metrics
# -----------------------------------------

mae = mean_absolute_error(
    evaluation_df["demand"],
    evaluation_df["forecast"]
)

rmse = np.sqrt(
    mean_squared_error(
        evaluation_df["demand"],
        evaluation_df["forecast"]
    )
)

mape = (
    evaluation_df["absolute_error"]
    / evaluation_df["demand"].replace(0, np.nan)
).mean() * 100

bias = evaluation_df["error"].mean()


# -----------------------------------------
# 5. Print results
# -----------------------------------------

print("\n========== NAIVE BASELINE ==========")

print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Bias: {bias:.2f}")


# -----------------------------------------
# 6. Show sample forecasts
# -----------------------------------------

print("\n========== SAMPLE FORECASTS ==========")

print(
    evaluation_df[
        [
            "date",
            "demand",
            "forecast",
            "error"
        ]
    ].head(10)
)