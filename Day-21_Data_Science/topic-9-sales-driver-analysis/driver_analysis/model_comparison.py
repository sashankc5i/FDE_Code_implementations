import pandas as pd
import numpy as np

from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso
)

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
# 4. Define models
# -----------------------------------------

models = {

    "Multiple Regression":
        LinearRegression(),

    "Ridge":
        Pipeline([
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                Ridge(alpha=1.0)
            )
        ]),

    "Lasso":
        Pipeline([
            (
                "scaler",
                StandardScaler()
            ),
            (
                "model",
                Lasso(alpha=1.0)
            )
        ])
}


# -----------------------------------------
# 5. Evaluate models
# -----------------------------------------

results = []


for name, model in models.items():

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

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

    results.append({
        "Model": name,
        "R2": r2,
        "MAE": mae,
        "RMSE": rmse
    })


# -----------------------------------------
# 6. Create comparison table
# -----------------------------------------

results_df = pd.DataFrame(
    results
)


# -----------------------------------------
# 7. Sort by MAE
# -----------------------------------------

results_df = results_df.sort_values(
    "MAE"
).reset_index(drop=True)


# -----------------------------------------
# 8. Print comparison
# -----------------------------------------

print(
    "\n========== DRIVER MODEL COMPARISON =========="
)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 9. Save comparison
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/driver_model_comparison.csv"
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nComparison saved to: {OUTPUT_PATH}"
)