import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


# -----------------------------------------
# 1. Load prepared data
# -----------------------------------------

DATA_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

df = pd.read_csv(DATA_PATH)


# -----------------------------------------
# 2. Define features
# -----------------------------------------

FEATURES = [
    "price",
    "promotion",
    "holiday",
    "promotion_price_interaction",
    "day_of_week",
    "month",
    "day_of_year",
    "trend"
]

TARGET = "demand"


# -----------------------------------------
# 3. Time-ordered train/test split
# -----------------------------------------

split_index = int(
    len(df) * 0.80
)

train = df.iloc[:split_index]
test = df.iloc[split_index:]


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
# 5. Generate predictions
# -----------------------------------------

predictions = model.predict(
    X_test
)


# -----------------------------------------
# 6. Calculate residuals
# -----------------------------------------

residuals = (
    y_test.values - predictions
)


# -----------------------------------------
# 7. Evaluation metrics
# -----------------------------------------

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


print(
    "\n========== RESIDUAL DIAGNOSTICS =========="
)

print(
    f"MAE:  {mae:.4f}"
)

print(
    f"RMSE: {rmse:.4f}"
)

print(
    f"Mean Residual: {residuals.mean():.4f}"
)

print(
    f"Residual Std:  {residuals.std():.4f}"
)


# -----------------------------------------
# 8. Residual summary
# -----------------------------------------

residual_summary = pd.DataFrame({
    "residual": residuals
})

print(
    "\nResidual Summary:"
)

print(
    residual_summary.describe()
)


# -----------------------------------------
# 9. Residual vs predicted plot
# -----------------------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    predictions,
    residuals,
    alpha=0.5
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel(
    "Predicted Demand"
)

plt.ylabel(
    "Residual"
)

plt.title(
    "Residuals vs Predicted Demand"
)

plt.tight_layout()


OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/residuals_vs_predictions.png"
)

plt.savefig(
    OUTPUT_PATH,
    dpi=150
)

plt.close()


# -----------------------------------------
# 10. Residuals over time
# -----------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    test["date"],
    residuals
)

plt.axhline(
    y=0,
    linestyle="--"
)

plt.xlabel(
    "Date"
)

plt.ylabel(
    "Residual"
)

plt.title(
    "Residuals Over Time"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()


OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/residuals_over_time.png"
)

plt.savefig(
    OUTPUT_PATH,
    dpi=150
)

plt.close()


print(
    "\nResidual plots saved successfully."
)