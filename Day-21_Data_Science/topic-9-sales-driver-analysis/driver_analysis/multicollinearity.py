import pandas as pd
import numpy as np

from statsmodels.stats.outliers_influence import variance_inflation_factor


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

X = df[FEATURES].copy()


# -----------------------------------------
# 3. Add intercept
# -----------------------------------------

X_with_constant = X.copy()

X_with_constant.insert(
    0,
    "const",
    1
)


# -----------------------------------------
# 4. Calculate VIF
# -----------------------------------------

vif_results = []

for i, feature in enumerate(
    X_with_constant.columns
):

    vif = variance_inflation_factor(
        X_with_constant.values,
        i
    )

    vif_results.append({
        "Feature": feature,
        "VIF": vif
    })


vif_df = pd.DataFrame(
    vif_results
)


# -----------------------------------------
# 5. Remove intercept from interpretation
# -----------------------------------------

vif_df = vif_df[
    vif_df["Feature"] != "const"
].copy()


vif_df = vif_df.sort_values(
    "VIF",
    ascending=False
).reset_index(
    drop=True
)


# -----------------------------------------
# 6. Categorize VIF
# -----------------------------------------

def classify_vif(vif):

    if vif < 5:
        return "Low"

    elif vif < 10:
        return "Moderate"

    else:
        return "High"


vif_df["VIF_Level"] = (
    vif_df["VIF"]
    .apply(classify_vif)
)


# -----------------------------------------
# 7. Print results
# -----------------------------------------

print(
    "\n========== MULTICOLLINEARITY ANALYSIS =========="
)

print(
    vif_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# -----------------------------------------
# 8. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/vif_analysis.csv"
)

vif_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print(
    f"\nVIF analysis saved to: {OUTPUT_PATH}"
)