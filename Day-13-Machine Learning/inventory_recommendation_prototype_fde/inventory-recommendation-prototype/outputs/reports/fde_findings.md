# FDE Findings — Inventory Recommendation Prototype

## Base-case results
- SKUs evaluated: 18
- Recommendations reduced by feasibility constraints: 11
- SKUs where final inventory remains below target inventory after constraints: 11

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
