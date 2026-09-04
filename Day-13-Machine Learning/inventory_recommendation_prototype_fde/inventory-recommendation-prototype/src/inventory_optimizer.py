from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/inventory_inputs.csv"
REPORTS = ROOT / "outputs/reports"
CHARTS = ROOT / "outputs/charts"
REPORTS.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA)

def recommend(row, demand_multiplier=1.0):
    demand = row.forecast_demand * demand_multiplier
    safety = demand * row.safety_stock_pct
    target = demand + safety
    raw_order = max(0, target - row.current_inventory)

    # Feasible upper bounds.
    budget_limit = math.floor(row.budget / row.unit_cost)
    warehouse_limit = max(0, row.warehouse_capacity - row.current_inventory)

    max_feasible = min(
        row.max_order,
        budget_limit,
        warehouse_limit
    )

    # Round down to MOQ multiples so the order never violates the budget/capacity.
    if row.moq > 0:
        feasible_order = math.floor(max_feasible / row.moq) * row.moq
        # If raw recommendation is below MOQ, order zero rather than forcing an unnecessary purchase.
        if raw_order < row.moq:
            final_order = 0
        else:
            desired_moq_order = math.ceil(raw_order / row.moq) * row.moq
            final_order = min(desired_moq_order, feasible_order)
    else:
        final_order = min(raw_order, max_feasible)

    return pd.Series({
        "scenario_demand": demand,
        "safety_stock": safety,
        "target_inventory": target,
        "raw_order": raw_order,
        "budget_limit_units": budget_limit,
        "warehouse_limit_units": warehouse_limit,
        "max_feasible_order": max_feasible,
        "recommended_order": final_order,
        "estimated_cost": final_order * row.unit_cost,
        "post_order_inventory": row.current_inventory + final_order,
    })

# Base recommendation
base = df.apply(recommend, axis=1)
base_out = pd.concat([df, base.add_prefix("")], axis=1)
base_out["scenario"] = "base"
base_out.to_csv(REPORTS / "inventory_recommendations.csv", index=False)

# Scenario analysis
scenario_rows = []
for name, multiplier in [("low", 0.80), ("base", 1.00), ("high", 1.20)]:
    for _, row in df.iterrows():
        rec = recommend(row, multiplier)
        scenario_rows.append({
            "sku": row.sku,
            "scenario": name,
            "demand_multiplier": multiplier,
            "forecast_demand": rec.scenario_demand,
            "recommended_order": rec.recommended_order,
            "estimated_cost": rec.estimated_cost,
        })

scenarios = pd.DataFrame(scenario_rows)
scenarios.to_csv(REPORTS / "scenario_analysis.csv", index=False)

# What-if: supplier cost +15%, with the same forecast assumptions.
what_if_rows = []
for _, row in df.iterrows():
    changed = row.copy()
    changed["unit_cost"] = row.unit_cost * 1.15
    rec = recommend(changed, 1.0)
    what_if_rows.append({
        "sku": row.sku,
        "original_unit_cost": row.unit_cost,
        "what_if_unit_cost": changed.unit_cost,
        "recommended_order": rec.recommended_order,
        "estimated_cost": rec.estimated_cost,
        "budget_limit_units": rec.budget_limit_units,
    })

what_if = pd.DataFrame(what_if_rows)
what_if.to_csv(REPORTS / "what_if_analysis.csv", index=False)

# Visualization
pivot = scenarios.pivot(index="sku", columns="scenario", values="recommended_order").fillna(0)
pivot = pivot.reindex(columns=["low", "base", "high"])
ax = pivot.plot(kind="bar", figsize=(12, 5))
ax.set_title("Inventory Recommendation by Demand Scenario")
ax.set_xlabel("SKU")
ax.set_ylabel("Recommended Order Units")
plt.tight_layout()
plt.savefig(CHARTS / "recommendation_by_scenario.png", dpi=150)
plt.close()

# FDE findings
budget_capped = (base_out["recommended_order"] < base_out["raw_order"]).sum()
stockouts_risk = (base_out["post_order_inventory"] < base_out["target_inventory"]).sum()

report = f"""# FDE Findings — Inventory Recommendation Prototype

## Base-case results
- SKUs evaluated: {len(base_out)}
- Recommendations reduced by feasibility constraints: {budget_capped}
- SKUs where final inventory remains below target inventory after constraints: {stockouts_risk}

## Decision architecture
Forecast demand is an input to the decision engine, not the final business action.

The engine:
1. Calculates target inventory from forecast demand + safety stock.
2. Calculates the raw order requirement.
3. Applies budget, warehouse capacity, supplier maximum and MOQ constraints.
4. Produces the final feasible recommendation.

## Scenario analysis
Low, base and high demand scenarios use 0.80x, 1.00x and 1.20x demand assumptions.

## What-if analysis
A +15% supplier unit-cost scenario is evaluated to show how a changing business assumption can alter the feasible order quantity.

## FDE investigation checklist
If a customer reports a poor recommendation:
- Verify forecast accuracy separately from recommendation logic.
- Check whether constraints were correctly configured.
- Verify current inventory and warehouse capacity.
- Check supplier MOQ/max-order rules.
- Check budget inputs.
- Confirm the recommendation was actually executable by the supplier.
- Compare low/base/high scenarios.
- Re-run the decision with changed assumptions through what-if analysis.

## Core principle
A mathematically optimal decision is only useful when the objective, constraints and inputs represent the real business.
"""

(REPORTS / "fde_findings.md").write_text(report)
print("Created inventory recommendation outputs.")
print(base_out[["sku", "forecast_demand", "current_inventory", "raw_order", "recommended_order", "estimated_cost"]].head(10).to_string(index=False))
