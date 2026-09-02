import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    df["month"] = pd.to_datetime(df["month"])

    return df


def prepare_monthly_metrics(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            customers=("customers", "sum"),
            aov=("aov", "mean"),
            conversion_rate=("conversion_rate", "mean"),
            return_rate=("return_rate", "mean"),
            retention_rate=("retention_rate", "mean"),
        )
        .reset_index()
    )

    return monthly


def prepare_region_metrics(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            customers=("customers", "sum"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )


def prepare_segment_metrics(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("customer_type")
        .agg(
            revenue=("revenue", "sum"),
            orders=("orders", "sum"),
            customers=("customers", "sum"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )