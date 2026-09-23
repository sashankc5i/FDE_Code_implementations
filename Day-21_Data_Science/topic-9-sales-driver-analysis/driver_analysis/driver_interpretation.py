import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.inspection import permutation_importance


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
# 4. Train Ridge model
# -----------------------------------------

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),
    (
        "regressor",
        __import__(
            "sklearn.linear_model",
            fromlist=["Ridge"]
        ).Ridge(alpha=1.0)
    )
])

model.fit(
    X_train,
    y_train
)


# -----------------------------------------
# 5. Extract standardized coefficients
# -----------------------------------------

regressor = model.named_steps[
    "regressor"
]

coefficients = regressor.coef_


coefficient_df = pd.DataFrame({
    "Feature": FEATURES,
    "Standardized_Coefficient": coefficients
})


coefficient_df[
    "Absolute_Coefficient"
] = (
    coefficient_df[
        "Standardized_Coefficient"
    ].abs()
)


coefficient_df = coefficient_df.sort_values(
    "Absolute_Coefficient",
    ascending=False
).reset_index(
    drop=True
)


# -----------------------------------------
# 6. Calculate permutation importance
# -----------------------------------------

permutation = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=10,
    random_state=42,
    scoring="neg_mean_absolute_error"
)


importance_df = pd.DataFrame({
    "Feature": FEATURES,
    "Permutation_Importance":
        permutation.importances_mean
})


importance_df = importance_df.sort_values(
    "Permutation_Importance",
    ascending=False
).reset_index(
    drop=True
)


# -----------------------------------------
# 7. Merge interpretation outputs
# -----------------------------------------

interpretation_df = coefficient_df.merge(
    importance_df,
    on="Feature"
)


# -----------------------------------------
# 8. Print results
# -----------------------------------------

print(
    "\n========== DRIVER INTERPRETATION =========="
)

print(
    interpretation_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 9. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/driver_interpretation.csv"
)

interpretation_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nDriver interpretation saved to: "
    f"{OUTPUT_PATH}"
)