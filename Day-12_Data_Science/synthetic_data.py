import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

RANDOM_SEED = 42
N_CUSTOMERS = 10_000

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# Customer master attributes
# ============================================================

customer_id = [
    f"C{i:06d}"
    for i in range(1, N_CUSTOMERS + 1)
]

regions = rng.choice(
    ["North", "South", "East", "West"],
    size=N_CUSTOMERS,
    p=[0.22, 0.38, 0.18, 0.22]
)

customer_type = rng.choice(
    ["Consumer", "SMB", "Enterprise"],
    size=N_CUSTOMERS,
    p=[0.65, 0.25, 0.10]
)

acquisition_channel = rng.choice(
    ["Organic", "Paid Search", "Referral", "Social", "Partner"],
    size=N_CUSTOMERS,
    p=[0.30, 0.20, 0.20, 0.15, 0.15]
)


# ============================================================
# Tenure
# ============================================================

# Right-skewed tenure distribution.
# Most customers are relatively new, while a smaller group
# has been with the company for a long time.

tenure_months = np.clip(
    rng.gamma(
        shape=2.2,
        scale=10,
        size=N_CUSTOMERS
    ).round(),
    1,
    72
).astype(int)


# ============================================================
# Orders
# ============================================================

# Base order frequency.
# Longer-tenure customers tend to place more orders.

base_orders = (
    1
    + tenure_months * 0.18
)

# Customer-type effect
customer_type_multiplier = np.select(
    [
        customer_type == "Consumer",
        customer_type == "SMB",
        customer_type == "Enterprise"
    ],
    [
        1.0,
        1.4,
        2.2
    ]
)

# Region effect
region_multiplier = np.select(
    [
        regions == "North",
        regions == "South",
        regions == "East",
        regions == "West"
    ],
    [
        1.00,
        1.20,
        0.90,
        1.05
    ]
)

orders = (
    base_orders
    * customer_type_multiplier
    * region_multiplier
    + rng.normal(0, 2.5, N_CUSTOMERS)
)

orders = np.maximum(
    np.round(orders),
    1
).astype(int)


# ============================================================
# Discount
# ============================================================

# Discounts vary by acquisition channel.
# Paid/social customers receive somewhat higher discounts.

channel_discount = np.select(
    [
        acquisition_channel == "Organic",
        acquisition_channel == "Paid Search",
        acquisition_channel == "Referral",
        acquisition_channel == "Social",
        acquisition_channel == "Partner"
    ],
    [
        5,
        12,
        7,
        15,
        8
    ]
)

discount_pct = (
    channel_discount
    + rng.normal(0, 3, N_CUSTOMERS)
)

discount_pct = np.clip(
    discount_pct,
    0,
    30
).round(1)


# ============================================================
# Revenue per order
# ============================================================

# Enterprise customers have substantially higher order value.
# Discounts reduce effective revenue per order.

base_order_value = np.select(
    [
        customer_type == "Consumer",
        customer_type == "SMB",
        customer_type == "Enterprise"
    ],
    [
        1500,
        3000,
        8500
    ]
)

# Regional pricing / purchasing behavior
region_value_multiplier = np.select(
    [
        regions == "North",
        regions == "South",
        regions == "East",
        regions == "West"
    ],
    [
        1.00,
        1.10,
        0.90,
        1.05
    ]
)

order_value = (
    base_order_value
    * region_value_multiplier
    * (1 - discount_pct / 100)
    * rng.lognormal(
        mean=0,
        sigma=0.20,
        size=N_CUSTOMERS
    )
)


# ============================================================
# Revenue
# ============================================================

revenue = orders * order_value

revenue = np.round(
    revenue,
    2
)


# ============================================================
# Returns
# ============================================================

# Return probability increases slightly with order volume.

return_probability = np.clip(
    0.03 + (orders / 1000),
    0.02,
    0.15
)

returns = rng.binomial(
    orders,
    return_probability
)


# ============================================================
# Build DataFrame
# ============================================================

df = pd.DataFrame({
    "customer_id": customer_id,
    "region": regions,
    "customer_type": customer_type,
    "acquisition_channel": acquisition_channel,
    "tenure_months": tenure_months,
    "orders": orders,
    "discount_pct": discount_pct,
    "returns": returns,
    "revenue": revenue
})


# ============================================================
# Inject realistic data-quality issues
# ============================================================

# Missing values
missing_discount_idx = rng.choice(
    df.index,
    size=50,
    replace=False
)

df.loc[
    missing_discount_idx,
    "discount_pct"
] = np.nan


# Duplicate customer records
duplicate_rows = df.sample(
    n=20,
    random_state=RANDOM_SEED
)

df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)


# ============================================================
# Inject legitimate high-value customers
# ============================================================

high_value_idx = rng.choice(
    df.index,
    size=10,
    replace=False
)

df.loc[
    high_value_idx,
    "customer_type"
] = "Enterprise"

df.loc[
    high_value_idx,
    "orders"
] *= 3

df.loc[
    high_value_idx,
    "revenue"
] *= 3


# ============================================================
# Inject suspicious records
# ============================================================

suspicious_idx = rng.choice(
    df.index,
    size=5,
    replace=False
)

# Extremely high revenue relative to order count
df.loc[
    suspicious_idx,
    "revenue"
] *= 20


# ============================================================
# Save dataset
# ============================================================

df.to_csv(
    "data/raw/customers.csv",
    index=False
)


# ============================================================
# Basic confirmation
# ============================================================

print(f"Dataset shape: {df.shape}")
print(f"Saved to: customers.csv")
print()
print(df.head())