import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from scipy.stats import norm


# -----------------------------------------
# 1. Load data
# -----------------------------------------

DATA_PATH = "forecasting/data/demand_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# -----------------------------------------
# 2. Create time-based features
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

TARGET = "demand"


# -----------------------------------------
# 3. Time-ordered train/test split
# -----------------------------------------

split_index = int(len(df) * 0.80)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()


X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]


# -----------------------------------------
# 4. Train regression model
# -----------------------------------------

model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 5. Generate forecasts
# -----------------------------------------

train_predictions = model.predict(X_train)

test_predictions = model.predict(X_test)


# -----------------------------------------
# 6. Estimate residual uncertainty
# -----------------------------------------

train_residuals = (
    y_train.values
    - train_predictions
)

residual_std = np.std(
    train_residuals,
    ddof=1
)


# -----------------------------------------
# 7. Create 95% prediction intervals
# -----------------------------------------

z_score = norm.ppf(0.975)

margin = z_score * residual_std

test["forecast"] = test_predictions

test["lower_bound"] = (
    test["forecast"] - margin
)

test["upper_bound"] = (
    test["forecast"] + margin
)


# -----------------------------------------
# 8. Calculate forecast errors
# -----------------------------------------

test["error"] = (
    test["demand"]
    - test["forecast"]
)

test["absolute_error"] = (
    test["error"].abs()
)


# -----------------------------------------
# 9. Calculate metrics
# -----------------------------------------

mae = mean_absolute_error(
    y_test,
    test["forecast"]
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        test["forecast"]
    )
)

mape = (
    test["absolute_error"]
    / test["demand"].replace(0, np.nan)
).mean() * 100

bias = test["error"].mean()


# -----------------------------------------
# 10. Calculate interval coverage
# -----------------------------------------

inside_interval = (
    (test["demand"] >= test["lower_bound"])
    &
    (test["demand"] <= test["upper_bound"])
)

coverage = inside_interval.mean() * 100


# -----------------------------------------
# 11. Print results
# -----------------------------------------

print("\n========== FORECAST WITH UNCERTAINTY ==========")

print(f"MAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Bias: {bias:.2f}")

print(
    f"\nResidual standard deviation: "
    f"{residual_std:.2f}"
)

print(
    f"95% interval margin: "
    f"{margin:.2f}"
)

print(
    f"Prediction interval coverage: "
    f"{coverage:.2f}%"
)


# -----------------------------------------
# 12. Show forecasts and intervals
# -----------------------------------------

print("\n========== FORECAST SAMPLE ==========")

print(
    test[
        [
            "date",
            "demand",
            "forecast",
            "lower_bound",
            "upper_bound"
        ]
    ].head(10)
)


# -----------------------------------------
# 13. Save forecast output
# -----------------------------------------

OUTPUT_PATH = (
    "forecasting/"
    "outputs/forecast_with_intervals.csv"
)

test[
    [
        "date",
        "demand",
        "forecast",
        "lower_bound",
        "upper_bound"
    ]
].to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nForecast saved to: {OUTPUT_PATH}"
)