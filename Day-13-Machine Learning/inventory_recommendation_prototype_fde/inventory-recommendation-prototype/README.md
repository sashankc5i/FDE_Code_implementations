# Inventory Recommendation Prototype — FDE Hands-On

## Objective
Build a decision-support prototype that converts demand forecasts and inventory state into constrained purchase recommendations.

## Concepts demonstrated
- Recommendations
- Constraints
- Optimization
- Low / Base / High scenarios
- What-if analysis

## Run
```bash
pip install -r requirements.txt
python src/generate_data.py
python src/inventory_optimizer.py
```

## Pipeline
Demand forecast + current inventory + business constraints
→ raw recommendation
→ constrained optimization
→ scenario analysis
→ what-if analysis
→ final recommendation

## FDE investigation focus
The prototype separates:
1. Forecast/prediction
2. Recommendation logic
3. Constraint handling
4. Business decision

This is intentional: a bad recommendation does not automatically mean the forecast/model is bad.

## Outputs
- `outputs/reports/inventory_recommendations.csv`
- `outputs/reports/scenario_analysis.csv`
- `outputs/reports/what_if_analysis.csv`
- `outputs/reports/fde_findings.md`
- `outputs/charts/recommendation_by_scenario.png`
