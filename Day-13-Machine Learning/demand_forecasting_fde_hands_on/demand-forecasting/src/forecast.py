from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/demand.csv"
CHARTS = ROOT / "outputs/charts"
REPORTS = ROOT / "outputs/reports"
CHARTS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["date"]).sort_values("date").reset_index(drop=True)

# -----------------------------
# Exploration
# -----------------------------
plt.figure(figsize=(11, 5))
plt.plot(df["date"], df["demand"])
plt.title("Observed Daily Demand")
plt.xlabel("Date")
plt.ylabel("Units")
plt.tight_layout()
plt.savefig(CHARTS / "demand_history.png", dpi=150)
plt.close()

df["rolling_7"] = df["demand"].rolling(7).mean()
plt.figure(figsize=(11, 5))
plt.plot(df["date"], df["demand"], alpha=0.45, label="Observed")
plt.plot(df["date"], df["rolling_7"], label="7-day moving average")
plt.title("Demand and 7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Units")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS / "rolling_average.png", dpi=150)
plt.close()

# -----------------------------
# Feature engineering
# -----------------------------
feature_df = df.copy()
feature_df["dow"] = feature_df["date"].dt.dayofweek
feature_df["month"] = feature_df["date"].dt.month
feature_df["dayofyear"] = feature_df["date"].dt.dayofyear

for lag in [1, 7, 14, 28]:
    feature_df[f"lag_{lag}"] = feature_df["demand"].shift(lag)

feature_df["rolling_7"] = feature_df["demand"].shift(1).rolling(7).mean()
feature_df["rolling_28"] = feature_df["demand"].shift(1).rolling(28).mean()

features = [
    "promotion", "holiday", "dow", "month", "dayofyear",
    "lag_1", "lag_7", "lag_14", "lag_28", "rolling_7", "rolling_28"
]

model_df = feature_df.dropna().copy()

# Time split: earliest 80% train, latest 20% test.
split = int(len(model_df) * 0.80)
train = model_df.iloc[:split]
test = model_df.iloc[split:]

X_train, y_train = train[features], train["demand"]
X_test, y_test = test[features], test["demand"]

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=10,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)
pred = model.predict(X_test)

# Seasonal-naive baseline: same weekday one week earlier.
baseline = test["lag_7"].to_numpy()

mae_model = mean_absolute_error(y_test, pred)
rmse_model = np.sqrt(mean_squared_error(y_test, pred))
mae_baseline = mean_absolute_error(y_test, baseline)
rmse_baseline = np.sqrt(mean_squared_error(y_test, baseline))

metrics = pd.DataFrame([
    {"model": "Seasonal naive (7-day)", "MAE": mae_baseline, "RMSE": rmse_baseline},
    {"model": "Random Forest lag-feature model", "MAE": mae_model, "RMSE": rmse_model},
])
metrics.to_csv(REPORTS / "metrics.csv", index=False)

forecast = test[["date", "demand"]].copy()
forecast["baseline"] = baseline
forecast["model_forecast"] = pred
forecast.to_csv(REPORTS / "future_forecast.csv", index=False)

plt.figure(figsize=(11, 5))
plt.plot(test["date"], y_test.to_numpy(), label="Actual")
plt.plot(test["date"], baseline, label="Seasonal naive")
plt.plot(test["date"], pred, label="Model")
plt.title("Future-Period Forecast Evaluation")
plt.xlabel("Date")
plt.ylabel("Units")
plt.legend()
plt.tight_layout()
plt.savefig(CHARTS / "forecast_vs_actual.png", dpi=150)
plt.close()

winner = "Random Forest" if mae_model < mae_baseline else "Seasonal naive"

report = f"""# FDE Findings — Demand Forecasting

## Evaluation
- Test period starts: {test['date'].min().date()}
- Test period ends: {test['date'].max().date()}
- Model MAE: {mae_model:.2f} units
- Model RMSE: {rmse_model:.2f} units
- Seasonal-naive MAE: {mae_baseline:.2f} units
- Seasonal-naive RMSE: {rmse_baseline:.2f} units
- Better model by MAE: {winner}

## FDE interpretation
The evaluation deliberately uses a future time block rather than a random split. This answers the operational question:
"How well would the model have predicted a period that it had not seen?"

The dataset also contains promotion/holiday effects and stockout-like constraints. Observed demand is therefore not guaranteed to equal unconstrained customer demand.

## Investigation checklist
1. Check whether errors concentrate on promotions or holidays.
2. Check weekday-level residuals for missed weekly seasonality.
3. Inspect stockout periods separately.
4. Verify every feature would be available at prediction time.
5. Compare against the seasonal-naive baseline before adopting the model.
6. Translate forecast error into inventory, staffing, or capacity impact.

## Key FDE principle
Forecast the business process, not blindly the observed number.
"""
(REPORTS / "fde_findings.md").write_text(report)

print(metrics.to_string(index=False))
print(f"\nOutputs written under {ROOT / 'outputs'}")
