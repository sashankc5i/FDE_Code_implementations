from src.data_processing import (
    load_data,
    prepare_monthly_metrics,
    prepare_region_metrics,
    prepare_segment_metrics,
)

df = load_data(
    "data/raw/business_metrics.csv"
)

print("\nMONTHLY")
print(prepare_monthly_metrics(df).head())

print("\nREGION")
print(prepare_region_metrics(df))

print("\nSEGMENT")
print(prepare_segment_metrics(df))