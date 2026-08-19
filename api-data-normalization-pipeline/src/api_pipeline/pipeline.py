"""Main API data processing pipeline."""

from pathlib import Path

from api_pipeline.api_client import AsyncAPIClient
from api_pipeline.config import (
    get_api_base_url,
    get_api_timeout,
)
from api_pipeline.normalization import (
    normalize_addresses,
    normalize_companies,
    normalize_customers,
)
from api_pipeline.storage import (
    save_dataframe,
    save_json,
)


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


async def run_pipeline() -> None:
    """Run the complete API ingestion pipeline."""

    client = AsyncAPIClient(
        base_url=get_api_base_url(),
        timeout=get_api_timeout(),
    )

    # Fetch API data concurrently.
    responses = await client.fetch_multiple(
        [
            "users",
            "posts",
            "todos",
        ]
    )

    users = responses["users"]

    print(
        f"Fetched {len(users)} users."
    )

    print(
        f"Fetched {len(responses['posts'])} posts."
    )

    print(
        f"Fetched {len(responses['todos'])} todos."
    )

    # Save raw source data.
    save_json(
        users,
        RAW_DATA_DIR / "users.json",
    )

    # Normalize.
    customers_df = normalize_customers(
        users
    )

    addresses_df = normalize_addresses(
        users
    )

    companies_df = normalize_companies(
        users
    )

    # Save customers.
    save_dataframe(
        customers_df,
        PROCESSED_DIR / "customers.csv",
    )

    save_dataframe(
        customers_df,
        PROCESSED_DIR / "customers.parquet",
    )

    # Save addresses.
    save_dataframe(
        addresses_df,
        PROCESSED_DIR / "addresses.csv",
    )

    save_dataframe(
        addresses_df,
        PROCESSED_DIR / "addresses.parquet",
    )

    # Save companies.
    save_dataframe(
        companies_df,
        PROCESSED_DIR / "companies.csv",
    )

    save_dataframe(
        companies_df,
        PROCESSED_DIR / "companies.parquet",
    )

    print(
        "\nPipeline completed successfully."
    )

    print(
        f"Customers: {len(customers_df)}"
    )

    print(
        f"Addresses: {len(addresses_df)}"
    )

    print(
        f"Companies: {len(companies_df)}"
    )