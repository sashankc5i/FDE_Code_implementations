import pandas as pd
import numpy as np

from sklearn.linear_model import Lasso
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


# -----------------------------------------
# 1. Load prepared data
# -----------------------------------------

DATA_PATH = (
    "topic-9-sales-driver-analysis/"
    "data/driver_data.csv"
)

df = pd.read_csv(DATA_PATH)


# -----------------------------------------
# 2. Define business drivers
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

train = df.iloc[:split_index].copy()

test = df.iloc[split_index:].copy()


X_train = train[FEATURES]

y_train = train[TARGET]

X_test = test[FEATURES]

y_test = test[TARGET]


# -----------------------------------------
# 4. Build Lasso pipeline
# -----------------------------------------

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "lasso",
        Lasso(alpha=1.0)
    )
])


# -----------------------------------------
# 5. Train model
# -----------------------------------------

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 6. Generate predictions
# -----------------------------------------

predictions = model.predict(
    X_test
)


# -----------------------------------------
# 7. Calculate metrics
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
# 8. Print performance
# -----------------------------------------

print(
    "\n========== LASSO REGRESSION =========="
)

print(
    "Regularization strength (alpha): 1.0"
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
# 9. Extract standardized coefficients
# -----------------------------------------

lasso_model = model.named_steps["lasso"]

coefficients = pd.DataFrame({
    "feature": FEATURES,
    "standardized_coefficient":
        lasso_model.coef_
})

coefficients["absolute_coefficient"] = (
    coefficients[
        "standardized_coefficient"
    ].abs()
)

coefficients = coefficients.sort_values(
    "absolute_coefficient",
    ascending=False
)


# -----------------------------------------
# 10. Print coefficients
# -----------------------------------------

print(
    "\n========== STANDARDIZED LASSO COEFFICIENTS =========="
)

print(
    coefficients[
        [
            "feature",
            "standardized_coefficient"
        ]
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 11. Identify zero coefficients
# -----------------------------------------

zero_features = coefficients[
    coefficients[
        "standardized_coefficient"
    ].abs() < 1e-8
]["feature"].tolist()


print(
    "\n========== FEATURE SELECTION =========="
)

if zero_features:
    print(
        "Features reduced to zero:"
    )

    for feature in zero_features:
        print(f"- {feature}")

else:
    print(
        "No features were reduced to zero."
    )


# -----------------------------------------
# 12. Save predictions
# -----------------------------------------

results = test[
    [
        "date",
        "demand"
    ]
].copy()

results["predicted_demand"] = predictions

results["residual"] = (
    results["demand"]
    - results["predicted_demand"]
)


OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/lasso_regression.csv"
)

results.to_csv(
    OUTPUT_PATH,
    index=False
)


# -----------------------------------------
# 13. Save coefficients
# -----------------------------------------

COEFFICIENT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/lasso_coefficients.csv"
)

coefficients[
    [
        "feature",
        "standardized_coefficient"
    ]
].to_csv(
    COEFFICIENT_PATH,
    index=False
)


print(
    f"\nPredictions saved to: {OUTPUT_PATH}"
)

print(
    f"Coefficients saved to: "
    f"{COEFFICIENT_PATH}"
)