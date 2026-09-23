import pandas as pd


# -----------------------------------------
# 1. Load driver interpretation results
# -----------------------------------------

INPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/driver_interpretation.csv"
)

df = pd.read_csv(
    INPUT_PATH
)


# -----------------------------------------
# 2. Classify evidence
# -----------------------------------------

def classify_evidence(feature):

    causal_warning = (
        "Predictive association only; "
        "causal impact not established."
    )

    if feature == "promotion":
        return causal_warning

    elif feature == "price":
        return causal_warning

    elif feature == "holiday":
        return causal_warning

    elif feature == "day_of_week":
        return causal_warning

    elif feature == "trend":
        return causal_warning

    elif feature == "month":
        return causal_warning

    elif feature == "day_of_year":
        return causal_warning

    elif feature == "promotion_price_interaction":
        return causal_warning

    return causal_warning


df["Interpretation"] = (
    df["Feature"]
    .apply(classify_evidence)
)


# -----------------------------------------
# 3. Add business interpretation
# -----------------------------------------

def business_context(feature):

    context = {

        "promotion":
            "Strong predictive association with demand.",

        "price":
            "Negative predictive association with demand.",

        "holiday":
            "Calendar-related demand association.",

        "day_of_week":
            "Weekly demand pattern.",

        "trend":
            "Long-term demand movement.",

        "month":
            "Monthly seasonal pattern.",

        "day_of_year":
            "Annual calendar progression.",

        "promotion_price_interaction":
            "Interaction between promotion status and price."
    }

    return context.get(
        feature,
        "Requires further investigation."
    )


df["Business_Context"] = (
    df["Feature"]
    .apply(business_context)
)


# -----------------------------------------
# 4. Create final interpretation table
# -----------------------------------------

final_df = df[
    [
        "Feature",
        "Standardized_Coefficient",
        "Permutation_Importance",
        "Business_Context",
        "Interpretation"
    ]
].copy()


# -----------------------------------------
# 5. Save output
# -----------------------------------------

OUTPUT_PATH = (
    "topic-9-sales-driver-analysis/"
    "outputs/association_vs_causation.csv"
)

final_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# -----------------------------------------
# 6. Print result
# -----------------------------------------

print(
    "\n========== ASSOCIATION VS CAUSATION =========="
)

print(
    final_df.to_string(
        index=False
    )
)

print(
    "\nImportant:"
)

print(
    "These results identify predictive associations "
    "and model relationships."
)

print(
    "They do NOT establish that any driver causes "
    "changes in demand."
)

print(
    f"\nOutput saved to: {OUTPUT_PATH}"
)