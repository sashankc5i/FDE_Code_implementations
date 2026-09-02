# Phase 1 — Data Quality Findings

## Objective
Assess whether the customer dataset is structurally and analytically reliable enough for customer-level analysis.

## Dataset Profile
- Rows: **10,020**
- Columns: **9**
- Intended grain: **one row per customer**
- Business key: `customer_id`
- Unique customers: **10,000**

## Missing Values
Only `discount_pct` contains missing values:
- Missing: **50**
- Missing percentage: **~0.5%**

All other columns contain no missing values.

Missing discount values should be handled according to the analytical question; they should not automatically be replaced with zero.

## Duplicate Records
- Exact duplicate rows: **20**
- Duplicate `customer_id` records: **20**

This violates the intended customer-level grain. The duplicate records appear to be exact copies.

**Action:** resolve duplicates before customer-level aggregation or analysis.

## Business Rule Validation
No invalid values were found for orders, returns, discount, revenue, or tenure.

## Revenue Sanity and Outliers
A derived metric, `revenue_per_order = revenue / orders`, was examined:
- Median: **~₹1,643**
- Mean: **~₹2,491**
- Maximum: **~₹57,007**

The mean being substantially above the median indicates right-skew. Extreme observations are candidates for investigation, not automatic deletion.

## Overall Assessment
The dataset is **usable but not fully clean**.

Before customer-level analysis:
1. Resolve the 20 duplicate customer records.
2. Decide how to handle the 50 missing discount values.
3. Investigate extreme revenue/order observations.
4. Preserve legitimate high-value customers unless evidence shows they are erroneous.

## FDE Takeaway
> Data quality is not simply checking whether values are null or invalid. It is determining whether the dataset's structure, grain, values, and business meaning are reliable enough for the decision being made.
