import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)


# -----------------------------------------
# 1. Load prepared data
# -----------------------------------------

DATA_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

df = pd.read_csv(DATA_PATH)


# -----------------------------------------
# 2. Define baseline driver
# -----------------------------------------

FEATURES = [
    "price"
]

TARGET = "demand"


# -----------------------------------------
# 3. Time-ordered train/test split
# -----------------------------------------

split_index = int(
    len(df) * 0.80
)

train = df.iloc[:split_index].copy()

test = df.iloc[split_index:].copy()


X_train = train[FEATURES]

y_train = train[TARGET]

X_test = test[FEATURES]

y_test = test[TARGET]


# -----------------------------------------
# 4. Train regression
# -----------------------------------------

model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 5. Generate predictions
# -----------------------------------------

predictions = model.predict(
    X_test
)


# -----------------------------------------
# 6. Calculate metrics
# -----------------------------------------

r2 = r2_score(
    y_test,
    predictions
)

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = np.sqrt(
    mean_squared_error(
        y_test,
        predictions
    )
)


# -----------------------------------------
# 7. Print performance
# -----------------------------------------

print(
    "\n========== BASELINE REGRESSION =========="
)

print(
    f"Feature: {FEATURES}"
)

print(
    f"\nR²:   {r2:.4f}"
)

print(
    f"MAE:  {mae:.2f}"
)

print(
    f"RMSE: {rmse:.2f}"
)


# -----------------------------------------
# 8. Print model equation
# -----------------------------------------

print(
    "\n========== MODEL COEFFICIENT =========="
)

print(
    f"Intercept: {model.intercept_:.4f}"
)

print(
    f"Price coefficient: "
    f"{model.coef_[0]:.4f}"
)


# -----------------------------------------
# 9. Show sample predictions
# -----------------------------------------

results = test[
    [
        "date",
        "demand",
        "price"
    ]
].copy()

results["predicted_demand"] = predictions

results["residual"] = (
    results["demand"]
    - results["predicted_demand"]
)


print(
    "\n========== SAMPLE PREDICTIONS =========="
)

print(
    results.head(10)
)


# -----------------------------------------
# 10. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/baseline_regression.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nResults saved to: {OUTPUT_PATH}"
)