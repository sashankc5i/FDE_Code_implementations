# Demand Forecasting — FDE Hands-On

## Goal
Build an end-to-end demand forecasting workflow that respects time order, compares a forecast with a simple baseline, evaluates future periods, and translates results into an operational recommendation.

## Project flow
Synthetic demand data → time-series exploration → seasonal-naive baseline → lag/rolling features → forecasting model → time-aware test → MAE/RMSE → forecast output → FDE interpretation

## Run
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/forecast.py
```

Outputs:
- `outputs/charts/demand_history.png`
- `outputs/charts/forecast_vs_actual.png`
- `outputs/charts/rolling_average.png`
- `outputs/reports/metrics.csv`
- `outputs/reports/future_forecast.csv`
- `outputs/reports/fde_findings.md`

## FDE traps intentionally represented
- Weekly seasonality
- Trend
- Promotion effects
- Random noise
- Stockout-like constrained observations

The project distinguishes observed sales from the possibility of unconstrained demand. Do not treat every low-sales period as low demand.
