import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def make_data(n=10000, seed=42):
    rng = np.random.default_rng(seed)
    age = rng.normal(38, 10, n).clip(18, 80)
    tenure = rng.exponential(24, n).clip(1, 120)
    sessions = rng.poisson(8, n)
    tickets = rng.poisson(1.5, n)
    orders = rng.poisson(3, n)
    discount = rng.beta(2, 5, n)
    days = rng.exponential(18, n).clip(0, 180)
    email = rng.beta(4, 3, n)
    logit = (-3.0 - .045*sessions - .18*orders + .025*days
             + .7*discount - .7*email + .10*tickets - .004*tenure)
    p = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, p)
    return pd.DataFrame({
        "age": age, "tenure_months": tenure, "sessions_30d": sessions,
        "support_tickets": tickets, "orders_90d": orders,
        "discount_use": discount, "days_since_purchase": days,
        "email_open_rate": email, "churn": churn
    })

def split_scale(df, seed=42):
    X, y = df.drop(columns="churn"), df["churn"]
    Xtr, Xtmp, ytr, ytmp = train_test_split(
        X, y, test_size=.30, random_state=seed, stratify=y)
    Xv, Xt, yv, yt = train_test_split(
        Xtmp, ytmp, test_size=.50, random_state=seed, stratify=ytmp)
    scaler = StandardScaler()
    return (scaler.fit_transform(Xtr), scaler.transform(Xv),
            scaler.transform(Xt), ytr.to_numpy(), yv.to_numpy(), yt.to_numpy())
