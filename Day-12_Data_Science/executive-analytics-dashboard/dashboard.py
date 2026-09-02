import streamlit as st
import plotly.express as px

from src.data_processing import (
    load_data,
    prepare_monthly_metrics,
    prepare_region_metrics,
    prepare_segment_metrics,
)


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Executive Business Health",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

DATA_PATH = "data/raw/business_metrics.csv"

df = load_data(DATA_PATH)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("Dashboard Filters")

regions = sorted(df["region"].unique())

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions,
)

customer_types = sorted(df["customer_type"].unique())

selected_customer_types = st.sidebar.multiselect(
    "Customer Type",
    customer_types,
    default=customer_types,
)


filtered_df = df[
    df["region"].isin(selected_regions)
    & df["customer_type"].isin(selected_customer_types)
]


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("Executive Business Health Dashboard")

st.caption(
    "Executive overview of revenue, customers, orders and business performance."
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["orders"].sum()

total_customers = filtered_df["customers"].sum()

overall_aov = (
    filtered_df["revenue"].sum()
    / filtered_df["orders"].sum()
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}",
    )

with col2:
    st.metric(
        "Total Orders",
        f"{total_orders:,.0f}",
    )

with col3:
    st.metric(
        "AOV",
        f"₹{overall_aov:,.0f}",
    )

with col4:
    st.metric(
        "Customers",
        f"{total_customers:,.0f}",
    )


st.divider()


# ---------------------------------------------------------
# MONTHLY METRICS
# ---------------------------------------------------------

monthly = prepare_monthly_metrics(filtered_df)


# ---------------------------------------------------------
# REVENUE TREND
# ---------------------------------------------------------

st.subheader("Revenue Trend")

fig_revenue = px.line(
    monthly,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue",
)

fig_revenue.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue",
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True,
)


# ---------------------------------------------------------
# REGIONAL + SEGMENT ANALYSIS
# ---------------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# REGION
# ---------------------------------------------------------

with col1:

    region_metrics = prepare_region_metrics(filtered_df)

    st.subheader("Revenue by Region")

    fig_region = px.bar(
        region_metrics,
        x="region",
        y="revenue",
        title="Revenue by Region",
        text_auto=".2s",
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue",
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True,
    )


# ---------------------------------------------------------
# CUSTOMER SEGMENT
# ---------------------------------------------------------

with col2:

    segment_metrics = prepare_segment_metrics(filtered_df)

    st.subheader("Revenue by Customer Type")

    fig_segment = px.bar(
        segment_metrics,
        x="customer_type",
        y="revenue",
        title="Revenue by Customer Type",
        text_auto=".2s",
    )

    fig_segment.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Revenue",
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True,
    )


# ---------------------------------------------------------
# DIAGNOSTIC METRICS
# ---------------------------------------------------------

st.divider()

st.subheader("Business Health Metrics")


col1, col2, col3, col4 = st.columns(4)

avg_conversion = filtered_df["conversion_rate"].mean()

avg_return = filtered_df["return_rate"].mean()

avg_retention = filtered_df["retention_rate"].mean()

avg_discount = filtered_df["discount_pct"].mean()


with col1:
    st.metric(
        "Conversion Rate",
        f"{avg_conversion:.2%}",
    )

with col2:
    st.metric(
        "Return Rate",
        f"{avg_return:.2%}",
    )

with col3:
    st.metric(
        "Retention Rate",
        f"{avg_retention:.2%}",
    )

with col4:
    st.metric(
        "Average Discount",
        f"{avg_discount:.2f}%",
    )


# ---------------------------------------------------------
# HEALTH TRENDS
# ---------------------------------------------------------

st.subheader("Business Health Trends")

health_metric = st.selectbox(
    "Select metric",
    [
        "conversion_rate",
        "return_rate",
        "retention_rate",
        "aov",
    ],
)


fig_health = px.line(
    monthly,
    x="month",
    y=health_metric,
    markers=True,
    title=f"{health_metric.replace('_', ' ').title()} Over Time",
)

fig_health.update_layout(
    xaxis_title="Month",
    yaxis_title=health_metric.replace("_", " ").title(),
)

st.plotly_chart(
    fig_health,
    use_container_width=True,
)


# ---------------------------------------------------------
# RAW DATA
# ---------------------------------------------------------

with st.expander("View underlying data"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
    )