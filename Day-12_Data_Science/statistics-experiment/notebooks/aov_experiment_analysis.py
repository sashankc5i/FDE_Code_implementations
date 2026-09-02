import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv("data/raw/experiment_aov.csv")

print("Shape:", df.shape)

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicates:", df.duplicated().sum())
print("Duplicate customer IDs:", df["customer_id"].duplicated().sum())

print("\nExperiment groups:")
print(df["experiment_group"].value_counts())

print("\nGroup statistics:")
print(
    df.groupby("experiment_group")["aov"]
      .agg(["count", "mean", "median", "std", "var", "min", "max"])
)
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

for group in ["Control", "Treatment"]:
    plt.hist(
        df.loc[df["experiment_group"] == group, "aov"],
        bins=60,
        alpha=0.5,
        label=group
    )

plt.xlabel("AOV")
plt.ylabel("Frequency")
plt.title("AOV Distribution — Control vs Treatment")
plt.legend()
plt.show()
plt.figure(figsize=(10, 6))

for group in ["Control", "Treatment"]:
    values = df.loc[df["experiment_group"] == group, "aov"]
    plt.hist(np.log1p(values), bins=60, alpha=0.5, label=group)

plt.xlabel("log(1 + AOV)")
plt.ylabel("Frequency")
plt.title("Log-Transformed AOV Distribution")
plt.legend()
plt.show()
control_mean = df.loc[
    df["experiment_group"] == "Control", "aov"
].mean()

treatment_mean = df.loc[
    df["experiment_group"] == "Treatment", "aov"
].mean()

absolute_difference = treatment_mean - control_mean

relative_difference = (
    absolute_difference / control_mean
) * 100

print("Control mean:", control_mean)
print("Treatment mean:", treatment_mean)
print("Absolute difference:", absolute_difference)
print("Relative difference (%):", relative_difference)
control = df.loc[
    df["experiment_group"] == "Control", "aov"
]

treatment = df.loc[
    df["experiment_group"] == "Treatment", "aov"
]

result = stats.ttest_ind(
    treatment,
    control,
    equal_var=False
)

print("t-statistic:", result.statistic)
print("p-value:", result.pvalue)
n_t = len(treatment)
n_c = len(control)

mean_diff = treatment.mean() - control.mean()

se = np.sqrt(
    treatment.var(ddof=1) / n_t +
    control.var(ddof=1) / n_c
)

df_welch = (
    (
        treatment.var(ddof=1) / n_t +
        control.var(ddof=1) / n_c
    ) ** 2
    /
    (
        (treatment.var(ddof=1) / n_t) ** 2 / (n_t - 1)
        +
        (control.var(ddof=1) / n_c) ** 2 / (n_c - 1)
    )
)

t_critical = stats.t.ppf(
    0.975,
    df_welch
)

margin_of_error = t_critical * se

ci_lower = mean_diff - margin_of_error
ci_upper = mean_diff + margin_of_error

print("Mean difference:", mean_diff)
print("95% CI:", (ci_lower, ci_upper))
segment_result = (
    df.groupby(["customer_type", "experiment_group"])["aov"]
      .agg(["count", "mean", "median", "std"])
)

print(segment_result)
region_result = (
    df.groupby(["region", "experiment_group"])["aov"]
      .agg(["count", "mean", "median", "std"])
)

print(region_result)
print("Control mean:", control_mean)
print("Treatment mean:", treatment_mean)
print("Absolute difference:", absolute_difference)
print("Relative difference (%):", relative_difference)
print("95% CI:", (ci_lower, ci_upper))
print("t-statistic:", result.statistic)
print("p-value:", result.pvalue)