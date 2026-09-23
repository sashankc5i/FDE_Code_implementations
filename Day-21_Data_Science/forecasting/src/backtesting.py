import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


# -----------------------------------------
# 1. Load data
# -----------------------------------------

DATA_PATH = "forecasting/data/demand_data.csv"

df = pd.read_csv(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

df = df.sort_values("date").reset_index(drop=True)


# -----------------------------------------
# 2. Create time-based features
# -----------------------------------------

df["day_of_week"] = df["date"].dt.dayofweek
df["month"] = df["date"].dt.month
df["day_of_year"] = df["date"].dt.dayofyear
df["trend"] = np.arange(len(df))


FEATURES = [
    "price",
    "promotion",
    "holiday",
    "day_of_week",
    "month",
    "day_of_year",
    "trend"
]

TARGET = "demand"


# -----------------------------------------
# 3. Backtesting configuration
# -----------------------------------------

initial_train_size = 700

forecast_horizon = 30

step_size = 30


results = []


# -----------------------------------------
# 4. Walk-forward validation
# -----------------------------------------

start = initial_train_size

while start + forecast_horizon <= len(df):

    train = df.iloc[:start]

    test = df.iloc[
        start:start + forecast_horizon
    ]

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]


    # -----------------------------
    # Train model
    # -----------------------------

    model = LinearRegression()

    model.fit(
        X_train,
        y_train
    )


    # -----------------------------
    # Forecast future period
    # -----------------------------

    forecast = model.predict(
        X_test
    )


    # -----------------------------
    # Calculate errors
    # -----------------------------

    errors = y_test.values - forecast

    mae = mean_absolute_error(
        y_test,
        forecast
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            forecast
        )
    )

    mape = (
        np.abs(errors)
        / np.where(
            y_test.values == 0,
            np.nan,
            y_test.values
        )
    ).mean() * 100

    bias = errors.mean()


    # -----------------------------
    # Store results
    # -----------------------------

    results.append({
        "train_end_date": train["date"].iloc[-1],
        "test_start_date": test["date"].iloc[0],
        "test_end_date": test["date"].iloc[-1],
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "Bias": bias
    })


    # Move forward
    start += step_size


# -----------------------------------------
# 5. Convert results to DataFrame
# -----------------------------------------

results_df = pd.DataFrame(results)


# -----------------------------------------
# 6. Print individual backtests
# -----------------------------------------

print("\n========== WALK-FORWARD BACKTEST ==========")

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}"
    )
)


# -----------------------------------------
# 7. Overall backtest performance
# -----------------------------------------

print("\n========== BACKTEST SUMMARY ==========")

print(
    f"Average MAE:  "
    f"{results_df['MAE'].mean():.2f}"
)

print(
    f"Average RMSE: "
    f"{results_df['RMSE'].mean():.2f}"
)

print(
    f"Average MAPE: "
    f"{results_df['MAPE'].mean():.2f}%"
)

print(
    f"Average Bias: "
    f"{results_df['Bias'].mean():.2f}"
)


# -----------------------------------------
# 8. Save results
# -----------------------------------------

OUTPUT_PATH = (
    "forecasting/"
    "outputs/backtesting_results.csv"
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nResults saved to: {OUTPUT_PATH}"
)