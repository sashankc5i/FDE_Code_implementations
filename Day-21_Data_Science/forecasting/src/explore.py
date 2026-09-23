import pandas as pd
import matplotlib.pyplot as plt


DATA_PATH = "forecasting/data/demand_data.csv"


# -----------------------------------------
# 1. Load data
# -----------------------------------------

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date")


# -----------------------------------------
# 2. Basic validation
# -----------------------------------------

print("\n========== DATASET INFO ==========")

print(f"Rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())


# -----------------------------------------
# 3. Date validation
# -----------------------------------------

print("\n========== DATE RANGE ==========")

print(f"Start: {df['date'].min()}")
print(f"End:   {df['date'].max()}")

date_diff = df["date"].diff().dropna()

print("\nDate frequency:")
print(date_diff.value_counts().head())


# -----------------------------------------
# 4. Demand statistics
# -----------------------------------------

print("\n========== DEMAND ==========")

print(df["demand"].describe())


# -----------------------------------------
# 5. Business variables
# -----------------------------------------

print("\n========== BUSINESS VARIABLES ==========")

print(df[[
    "price",
    "promotion",
    "holiday"
]].describe())


# -----------------------------------------
# 6. Plot demand
# -----------------------------------------

plt.figure(figsize=(14, 6))

plt.plot(
    df["date"],
    df["demand"]
)

plt.title("Daily Demand")
plt.xlabel("Date")
plt.ylabel("Demand")

plt.tight_layout()

plt.savefig(
    "forecasting/outputs/demand_over_time.png"
)

plt.show()