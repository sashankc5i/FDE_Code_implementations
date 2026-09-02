# Phase 2 — Diagnostic Analytics Findings

## Objective
Move from describing what happened to determining **why it happened**, using segmentation, relationships, outlier investigation, and competing hypotheses.

## Diagnostic Framework
**Business symptom → Define metric → Validate → EDA → Distribution → Relationships → Segmentation → Outlier investigation → Hypotheses → Test alternatives → Quantify contribution → Identify business driver → Recommend action**

## Observation vs Relationship vs Hypothesis vs Evidence
- **Observation:** Revenue increased.
- **Relationship:** Customers with more orders tend to generate more revenue.
- **Hypothesis:** Increased purchase frequency may be driving revenue growth.
- **Evidence:** Quantifying segment contributions and comparing affected vs unaffected populations supports or challenges the hypothesis.
- **Business driver:** The factor best supported as materially contributing to the outcome.
- **Recommendation:** Translate the supported driver into an action.

## Segmentation
Useful dimensions include region, customer type, acquisition channel, tenure, order frequency, and discount level. Overall metrics can hide materially different segment behavior.

## Correlation
Correlation is useful for identifying relationships between variables such as orders, revenue, tenure, discount, and revenue per order.

> **Correlation does not establish causation.**

A correlation is an investigative lead, not proof that one variable causes another.

## Outlier Investigation
Outliers should not automatically be deleted. The process is:
1. Identify the observation.
2. Validate the underlying record.
3. Determine whether it is legitimate.
4. Assess its influence on the metric.
5. Decide whether to retain, transform, or exclude it.
6. Document the decision.

## Root-Cause Reasoning
Ask:
1. What changed?
2. Where did it change?
3. Which population contributed to the change?
4. What factors are associated with that population?
5. Which competing explanation is best supported by evidence?

## FDE Investigation Pattern
For a claim such as **"Revenue has changed significantly"**:
1. Define the metric and comparison period.
2. Validate the data.
3. Explore the distribution.
4. Segment the population.
5. Compare affected and unaffected groups.
6. Investigate relationships.
7. Form multiple hypotheses.
8. Test competing explanations.
9. Quantify segment contribution.
10. Identify the strongest evidence-supported driver.
11. Recommend an action.

## Key Lessons
- Revenue growth does not automatically mean customer growth; it can come from more customers, more orders, higher AOV, mix changes, pricing, discounts, or other factors.
- High-value customers require context; a large value may be legitimate.
- Diagnostic analytics identifies potential drivers; statistical analysis helps assess whether observed differences are sufficiently supported by the data.

## FDE Takeaway
> The strongest diagnostic answer is not "Variable X has the highest correlation." It is "The business symptom is concentrated in population X, factor Y is associated with the change, competing explanations were investigated, and the evidence indicates Y is the strongest supported driver."
