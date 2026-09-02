# Phase 3 --- Data Visualization & Storytelling

## 1. Phase Overview

### Objective

The objective of Phase 3 was to learn how to transform analytical
results into effective visualizations, dashboards, and business stories.

The focus was not only on learning visualization libraries, but on
developing an FDE-oriented approach to communicating data:

**Business Question → Metric → Analytical Question → Visualization →
Pattern → Insight → Business Implication → Recommendation**

### Phase Status

**COMPLETED**

------------------------------------------------------------------------

## 2. Topics Covered

-   Visualization fundamentals
-   Chart selection
-   Matplotlib
-   Seaborn
-   Plotly
-   Interactive dashboards
-   KPI design
-   Dashboard hierarchy
-   Trend analysis
-   Comparative analysis
-   Distribution analysis
-   Relationship analysis
-   Segmentation
-   Diagnostic visualization
-   Data storytelling
-   Executive communication
-   FDE-oriented visualization

------------------------------------------------------------------------

# 3. Visualization Fundamentals

Visualization is an analytical tool rather than decoration.

The appropriate visualization depends on the business question being
answered.

  Analytical Question                          Recommended Visualization
  -------------------------------------------- ---------------------------
  How is something changing over time?         Line chart
  Which category is larger or smaller?         Bar chart
  What does the distribution look like?        Histogram
  What is the spread and are there outliers?   Box plot
  Are two variables related?                   Scatter plot
  How is a total composed?                     Stacked bar chart
  What is the current business state?          KPI card

### Core Principle

> Choose the visualization based on the analytical question, not based
> on the chart that looks most attractive.

------------------------------------------------------------------------

# 4. Visualization Hierarchy

For many business comparisons, visual encoding can be thought of roughly
in this order:

**Position → Length → Angle → Area**

This is one reason bar charts are generally more effective than pie
charts when users need to make precise comparisons between categories.

The goal is to reduce the cognitive effort required to interpret the
information.

------------------------------------------------------------------------

# 5. Trend Analysis

Time-series business metrics are generally well represented using line
charts.

Examples include:

-   Monthly revenue
-   Monthly orders
-   AOV over time
-   Conversion rate over time
-   Return rate over time
-   Retention rate over time

A trend visualization should help identify:

-   Growth
-   Decline
-   Sudden changes
-   Inflection points
-   Possible seasonality
-   Periods requiring investigation

The chart itself is not the final insight. It is evidence used to
support the investigation.

------------------------------------------------------------------------

# 6. Comparative Analysis

Bar charts are appropriate when comparing discrete categories.

Examples:

-   Revenue by region
-   Revenue by customer type
-   Orders by acquisition channel
-   Customers by segment

The main analytical objective is to identify relative differences and
prioritize where investigation may be required.

A key caution is avoiding misleading visual scales, such as
unnecessarily truncated axes that exaggerate small differences.

------------------------------------------------------------------------

# 7. Distribution Analysis

Distributions provide information that aggregate metrics can hide.

### Histogram

Useful for understanding:

-   Shape
-   Skew
-   Concentration
-   Multiple modes
-   Extreme values

### Box Plot

Useful for understanding:

-   Median
-   Interquartile range
-   Spread
-   Potential outliers

This connects directly to the statistical and diagnostic analysis
covered earlier.

For example, a large difference between mean and median can indicate a
skewed metric and should prompt further investigation.

------------------------------------------------------------------------

# 8. Relationship Analysis

Scatter plots can be used to examine relationships between numerical
variables.

Examples:

-   Orders vs revenue
-   Orders vs AOV
-   Discount vs revenue
-   Conversion rate vs revenue

A visualization may reveal a relationship, but:

> **Correlation does not establish causation.**

The visualization should therefore be treated as evidence for hypothesis
generation rather than automatic proof of a causal driver.

------------------------------------------------------------------------

# 9. Segmentation

Aggregate metrics can hide important business problems.

A business can appear healthy overall while a particular region,
customer segment, product category, or acquisition channel deteriorates.

The analytical pattern is:

**Overall Metric → Segment → Deviation → Investigation → Candidate
Driver**

Useful segmentation dimensions include:

-   Region
-   Customer type
-   Acquisition channel
-   Product/category
-   Time period

Segmentation is therefore a critical part of FDE-oriented dashboard
design.

------------------------------------------------------------------------

# 10. Dashboard Architecture

The dashboard was designed around an executive-to-diagnostic hierarchy.

``` text
Executive Question
        ↓
      KPI
        ↓
     Trend
        ↓
    Drivers
        ↓
   Segments
        ↓
    Details
```

This hierarchy keeps the dashboard focused.

An executive should first understand the current business state, then
the direction of movement, then where the movement is occurring, and
finally the evidence that helps explain it.

------------------------------------------------------------------------

# 11. Executive Business Health Dashboard

The hands-on deliverable for this phase was an **Executive Business
Health Dashboard**.

### Technology

-   Python
-   Pandas
-   Plotly
-   Streamlit

### Dataset

The dashboard uses a synthetic business dataset covering:

-   24 monthly periods
-   January 2024 through December 2025
-   Four regions
-   Three customer types

### Dimensions

-   Month
-   Region
-   Customer Type

### Metrics

-   Customers
-   Orders
-   AOV
-   Revenue
-   Conversion Rate
-   Return Rate
-   Retention Rate
-   Discount Percentage

------------------------------------------------------------------------

# 12. Dashboard Components

## Executive KPIs

The dashboard provides:

-   Total Revenue
-   Total Orders
-   AOV
-   Customers

These provide the initial high-level business health view.

## Revenue Trend

A monthly revenue trend provides the time-series view and helps identify
changes in overall business performance.

## Revenue by Region

Regional comparison helps identify geographic differences and potential
problem areas.

## Revenue by Customer Type

Customer-type comparison helps identify which segments contribute most
to the business.

## Business Health Metrics

Additional metrics include:

-   Conversion Rate
-   Return Rate
-   Retention Rate
-   Average Discount

These metrics provide diagnostic context around the primary revenue
outcome.

## Interactive Filtering

The dashboard supports filtering by:

-   Region
-   Customer Type

This enables users to move from aggregate performance into segment-level
analysis.

------------------------------------------------------------------------

# 13. Dashboard Implementation Architecture

The implementation separates data preparation from dashboard
presentation.

``` text
business_metrics.csv
        ↓
load_data()
        ↓
data_processing.py
        ↓
Prepared Business Metrics
        ↓
dashboard.py
        ↓
Streamlit
        ↓
Interactive Executive Dashboard
```

### Why the separation matters

Business logic should not be buried inside visualization code.

Separating processing from presentation provides:

-   Reusable transformations
-   Easier testing
-   Easier maintenance
-   Cleaner dashboard code
-   Ability to reuse metrics in other applications

The same processing layer could later support a report, API, notebook,
or another visualization application.

------------------------------------------------------------------------

# 14. Diagnostic Business Finding

The synthetic dataset contains a deliberately introduced regional
business signal.

The **South region begins showing deterioration from approximately July
2025**.

The important pattern is:

``` text
South Region
     ↓
Return Rate increases
     ↓
AOV decreases
     ↓
Potential revenue pressure
     ↓
Requires investigation
```

The important FDE interpretation is that this should not be reduced to:

> "South revenue is declining."

Instead, the dashboard enables a deeper investigation:

``` text
Business Outcome
      ↓
Revenue
      ↓
Region
      ↓
South
      ↓
AOV
      ↓
Return Rate
      ↓
Candidate Driver
```

This demonstrates why executive dashboards should contain both outcome
metrics and diagnostic metrics.

------------------------------------------------------------------------

# 15. Root-Cause Caution

The dashboard identifies a **pattern requiring investigation**.

It does not prove the ultimate root cause.

Potential areas for additional investigation include:

-   Product/category mix
-   Product quality
-   Customer experience
-   Fulfillment
-   Pricing
-   Regional operational changes
-   Return reasons

Additional operational or customer-level data would be required to
establish the confirmed root cause.

This distinction is important in FDE work:

> **Observed pattern ≠ confirmed root cause.**

------------------------------------------------------------------------

# 16. Storytelling Framework

The storytelling framework used in this phase is:

``` text
Observation
     ↓
Insight
     ↓
Business Implication
     ↓
Recommendation
```

### Observation

Identify what changed.

### Insight

Explain what the observed pattern means in context.

### Business Implication

Explain why the pattern matters to the customer.

### Recommendation

Suggest an action or investigation supported by the evidence.

A chart is therefore not the story.

The chart is evidence that supports the story.

------------------------------------------------------------------------

# 17. FDE Investigation Pattern

A practical FDE visualization investigation follows:

``` text
Customer Question
       ↓
Define Business Metric
       ↓
Validate Metric
       ↓
Visualize Overall Performance
       ↓
Identify Pattern / Anomaly
       ↓
Segment the Problem
       ↓
Identify Candidate Drivers
       ↓
Validate Hypothesis
       ↓
Explain Business Impact
       ↓
Recommend Action
```

This approach prevents dashboards from becoming collections of unrelated
charts.

Every visualization should contribute to answering a business question.

------------------------------------------------------------------------

# 18. Executive Dashboard Design Principles

## 1. Start with the business question

Instead of asking:

> Which chart should I create?

Ask:

> What decision does the customer need to make?

## 2. Prioritize information

Executives should quickly understand:

-   Current state
-   Direction of movement
-   Major problem areas

## 3. Combine outcome and diagnostic metrics

Revenue alone tells the customer **what happened**.

Metrics such as AOV, conversion, returns, retention, and discounting
help investigate **why it may have happened**.

## 4. Use segmentation

Overall averages can hide localized problems.

## 5. Avoid visual noise

Every chart should have a purpose.

## 6. Avoid misleading scales

Charts should represent differences honestly and avoid visual techniques
that exaggerate changes.

## 7. Use interactivity where it improves investigation

Filters should support exploration rather than become decoration.

------------------------------------------------------------------------

# 19. Tool-Specific Takeaways

## Matplotlib

Matplotlib provides low-level control over figures and axes.

Important concepts:

-   Figure
-   Axes
-   Line plots
-   Bar charts
-   Scatter plots
-   Histograms
-   Labels
-   Titles
-   Annotations

## Seaborn

Seaborn provides higher-level statistical visualization functionality
and integrates well with Pandas.

Useful visualizations include:

-   Histograms
-   Box plots
-   Scatter plots
-   Heatmaps

## Plotly

Plotly is useful when interactive exploration is valuable.

Features include:

-   Hover information
-   Zooming
-   Interactive exploration
-   Interactive charts
-   Dashboard integration

## Streamlit

Streamlit provides a fast way to turn Python analytical code into an
interactive application.

For an FDE workflow, it is useful for rapidly demonstrating analytical
findings to customers or internal stakeholders.

------------------------------------------------------------------------

# 20. FDE vs Traditional Visualization

A traditional visualization workflow may look like:

``` text
Dataset
  ↓
Charts
  ↓
Dashboard
```

An FDE-oriented workflow is:

``` text
Customer Problem
      ↓
Business Question
      ↓
Metric Definition
      ↓
Analytical Investigation
      ↓
Visualization
      ↓
Evidence
      ↓
Business Insight
      ↓
Recommended Action
```

The second approach is more useful because it connects technical
analysis directly to customer outcomes.

------------------------------------------------------------------------

# 21. Common Failure Modes

### Too many charts

More charts do not automatically provide more insight.

### Wrong chart type

A technically correct chart can still be a poor communication choice.

### KPI overload

Displaying every available metric can make it difficult to identify what
matters.

### No segmentation

Aggregate metrics may hide localized problems.

### No diagnostic metrics

A dashboard may show that something changed without helping explain why.

### Treating correlation as causation

A visible relationship should generate a hypothesis, not automatically
become a conclusion.

### Treating outliers as errors

Extreme values should be investigated before being removed.

### No business recommendation

A dashboard that stops at visualization does not complete the FDE
analytical workflow.

------------------------------------------------------------------------

# 22. Phase-Level FDE Takeaways

The most important learning from this phase is not the syntax of
Matplotlib, Seaborn, Plotly, or Streamlit.

The core takeaway is:

> **Visualization is an analytical interface between data and
> decision-making.**

An FDE should be able to determine:

1.  What business question needs to be answered?
2.  What metric represents the problem?
3.  What visualization makes the pattern clear?
4.  What segmentation is required?
5.  What additional metrics help explain the outcome?
6.  What evidence supports the conclusion?
7.  What action should the customer take?

The objective is not:

> Build a beautiful dashboard.

The objective is:

> Build a dashboard that makes the customer's problem easier to see,
> investigate, explain, and act upon.

------------------------------------------------------------------------

# 23. Final Phase Output

The completed Phase 3 workflow is:

``` text
Raw Business Data
       ↓
Data Processing
       ↓
Business Metrics
       ↓
Visualization
       ↓
Executive Dashboard
       ↓
Diagnostic Analysis
       ↓
Business Insight
       ↓
Recommendation
```

### Deliverables

  Deliverable                  Status
  ---------------------------- -----------
  Visualization fundamentals   Completed
  Matplotlib                   Covered
  Seaborn                      Covered
  Plotly                       Covered
  Chart selection              Completed
  Dashboard architecture       Completed
  Data processing layer        Completed
  Executive KPI layer          Completed
  Revenue trend                Completed
  Regional analysis            Completed
  Customer-segment analysis    Completed
  Business-health metrics      Completed
  Interactive filters          Completed
  Diagnostic analysis          Completed
  Storytelling framework       Completed
  FDE interpretation           Completed
  Executive dashboard          Completed
  Phase documentation          Completed

------------------------------------------------------------------------

# 24. Phase Closure

**Phase 3 --- Data Visualization & Storytelling: COMPLETED**

The phase successfully established the ability to move from analytical
data to executive communication while maintaining an FDE-oriented
investigation mindset.

The final capability demonstrated is:

**Customer Question → Metric → Analysis → Visualization → Pattern →
Evidence → Insight → Business Action**

This phase is considered closed.
