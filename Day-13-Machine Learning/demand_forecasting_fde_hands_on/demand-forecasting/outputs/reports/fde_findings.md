# FDE Findings — Demand Forecasting

## Evaluation
- Test period starts: 2025-12-08
- Test period ends: 2026-02-24
- Model MAE: 30.39 units
- Model RMSE: 40.68 units
- Seasonal-naive MAE: 38.66 units
- Seasonal-naive RMSE: 55.46 units
- Better model by MAE: Random Forest

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
