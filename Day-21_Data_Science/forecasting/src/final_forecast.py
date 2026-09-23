import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from scipy.stats import norm


# -----------------------------------------
# 1. Configuration
# -----------------------------------------

DATA_PATH = (
    "forecasting/"
    "data/demand_data.csv"
)

OUTPUT_PATH = (
    "forecasting/"
    "outputs/final_forecast.csv"
)

FORECAST_HORIZON = 30

CONFIDENCE_LEVEL = 0.95


# -----------------------------------------
# 2. Load historical data
# -----------------------------------------

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = (
    df
    .sort_values("date")
    .reset_index(drop=True)
)


# -----------------------------------------
# 3. Create model features
# -----------------------------------------

df["day_of_week"] = df["date"].dt.dayofweek

df["month"] = df["date"].dt.month

df["day_of_year"] = df["date"].dt.dayofyear

df["trend"] = np.arange(len(df))


FEATURES = [
    "price",
    "promotion",
    "holiday",
    "day_of_week",
    "month",
    "day_of_year",
    "trend"
]


# -----------------------------------------
# 4. Train final model
# -----------------------------------------

X_train = df[FEATURES]

y_train = df["demand"]


model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 5. Estimate residual uncertainty
# -----------------------------------------

train_predictions = model.predict(
    X_train
)

residuals = (
    y_train.values
    - train_predictions
)

residual_std = np.std(
    residuals,
    ddof=1
)


# -----------------------------------------
# 6. Generate future dates
# -----------------------------------------

last_date = df["date"].max()

future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=FORECAST_HORIZON,
    freq="D"
)


future = pd.DataFrame({
    "date": future_dates
})


# -----------------------------------------
# 7. Create future business features
# -----------------------------------------

future["day_of_week"] = (
    future["date"].dt.dayofweek
)

future["month"] = (
    future["date"].dt.month
)

future["day_of_year"] = (
    future["date"].dt.dayofyear
)

future["trend"] = np.arange(
    len(df),
    len(df) + FORECAST_HORIZON
)


# -----------------------------------------
# 8. Generate future business signals
# -----------------------------------------

# For this synthetic example:
# price follows the historical average
# promotion and holiday are assumed to be known
# for the forecast horizon.

future["price"] = df["price"].mean()

future["promotion"] = 0

future["holiday"] = (
    future["month"].isin([11, 12])
    & (future["day_of_week"] >= 5)
).astype(int)


# -----------------------------------------
# 9. Generate demand forecast
# -----------------------------------------

future["forecast"] = model.predict(
    future[FEATURES]
)


# -----------------------------------------
# 10. Create prediction interval
# -----------------------------------------

alpha = 1 - CONFIDENCE_LEVEL

z_score = norm.ppf(
    1 - alpha / 2
)

margin = (
    z_score
    * residual_std
)


future["lower_bound"] = (
    future["forecast"] - margin
)

future["upper_bound"] = (
    future["forecast"] + margin
)


# -----------------------------------------
# 11. Prevent negative forecasts
# -----------------------------------------

future["forecast"] = future["forecast"].clip(
    lower=0
)

future["lower_bound"] = future[
    "lower_bound"
].clip(
    lower=0
)


# -----------------------------------------
# 12. Select final output columns
# -----------------------------------------

final_forecast = future[
    [
        "date",
        "forecast",
        "lower_bound",
        "upper_bound"
    ]
].copy()


# -----------------------------------------
# 13. Save forecast
# -----------------------------------------

final_forecast.to_csv(
    OUTPUT_PATH,
    index=False
)


# -----------------------------------------
# 14. Print summary
# -----------------------------------------

print("\n========== FINAL FORECAST ==========")

print(
    f"Forecast horizon: "
    f"{FORECAST_HORIZON} days"
)

print(
    f"Confidence level: "
    f"{CONFIDENCE_LEVEL * 100:.0f}%"
)

print(
    f"Residual standard deviation: "
    f"{residual_std:.2f}"
)

print(
    f"Interval margin: "
    f"{margin:.2f}"
)

print("\nForecast sample:")

print(
    final_forecast.head(10)
)

print(
    f"\nForecast saved to: {OUTPUT_PATH}"
)