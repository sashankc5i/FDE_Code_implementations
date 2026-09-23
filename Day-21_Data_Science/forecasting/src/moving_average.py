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
# 2. Create 7-day moving average forecast
# -----------------------------------------

WINDOW = 7

df["forecast"] = (
    df["demand"]
    .rolling(window=WINDOW)
    .mean()
    .shift(1)
)


# -----------------------------------------
# 3. Remove rows without a forecast
# -----------------------------------------

evaluation_df = df.dropna(
    subset=["forecast"]
).copy()


# -----------------------------------------
# 4. Calculate forecast errors
# -----------------------------------------

evaluation_df["error"] = (
    evaluation_df["demand"]
    - evaluation_df["forecast"]
)

evaluation_df["absolute_error"] = (
    evaluation_df["error"].abs()
)


# -----------------------------------------
# 5. Calculate metrics
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
# 6. Print results
# -----------------------------------------

print("\n========== 7-DAY MOVING AVERAGE ==========")

print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Bias: {bias:.2f}")


# -----------------------------------------
# 7. Show sample forecasts
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