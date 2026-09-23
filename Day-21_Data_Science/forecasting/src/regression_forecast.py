import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


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


# -----------------------------------------
# 3. Define features
# -----------------------------------------

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
# 4. Time-ordered train/test split
# -----------------------------------------

split_index = int(len(df) * 0.80)

train = df.iloc[:split_index].copy()

test = df.iloc[split_index:].copy()


X_train = train[FEATURES]

y_train = train[TARGET]

X_test = test[FEATURES]

y_test = test[TARGET]


# -----------------------------------------
# 5. Train regression model
# -----------------------------------------

model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 6. Generate forecasts
# -----------------------------------------

test["forecast"] = model.predict(
    X_test
)


# -----------------------------------------
# 7. Calculate forecast errors
# -----------------------------------------

test["error"] = (
    test["demand"]
    - test["forecast"]
)

test["absolute_error"] = (
    test["error"].abs()
)


# -----------------------------------------
# 8. Calculate metrics
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
# 9. Print model performance
# -----------------------------------------

print("\n========== REGRESSION FORECAST ==========")

print(f"Train rows: {len(train)}")
print(f"Test rows:  {len(test)}")

print(f"\nMAE:  {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Bias: {bias:.2f}")


# -----------------------------------------
# 10. Print coefficients
# -----------------------------------------

print("\n========== MODEL COEFFICIENTS ==========")

coefficients = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": model.coef_
})

coefficients["absolute_coefficient"] = (
    coefficients["coefficient"].abs()
)

print(
    coefficients.sort_values(
        "absolute_coefficient",
        ascending=False
    ).drop(
        columns=["absolute_coefficient"]
    )
)


# -----------------------------------------
# 11. Show sample forecasts
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