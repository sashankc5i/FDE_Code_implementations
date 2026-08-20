"""Integration tests for the API normalization pipeline."""

from pathlib import Path

import httpx
import pandas as pd
import pytest

from api_pipeline.api_client import AsyncAPIClient
from api_pipeline.normalization import (
    normalize_addresses,
    normalize_companies,
    normalize_customers,
)
from api_pipeline.storage import save_dataframe, save_json


def create_mock_users() -> list[dict]:
    """Create realistic API response data for integration testing."""

    return [
        {
            "id": 101,
            "name": "Arun",
            "username": "arun101",
            "email": "arun@example.com",
            "phone": "1234567890",
            "website": "arun.example.com",
            "address": {
                "street": "MG Road",
                "suite": "Apt. 101",
                "city": "Chennai",
                "zipcode": "600001",
                "geo": {
                    "lat": "13.0827",
                    "lng": "80.2707",
                },
            },
            "company": {
                "name": "ABC Technologies",
                "catchPhrase": "Building better systems",
                "bs": "technology solutions",
            },
        },
        {
            "id": 102,
            "name": "Priya",
            "username": "priya102",
            "email": "priya@example.com",
            "phone": "9876543210",
            "website": "priya.example.com",
            "address": {
                "street": "Anna Salai",
                "suite": "Suite 202",
                "city": "Coimbatore",
                "zipcode": "641001",
                "geo": {
                    "lat": "11.0168",
                    "lng": "76.9558",
                },
            },
            "company": {
                "name": "XYZ Solutions",
                "catchPhrase": "Simplifying business",
                "bs": "business solutions",
            },
        },
    ]


@pytest.mark.asyncio
async def test_api_normalization_pipeline(
    tmp_path: Path,
):
    """
    Test the complete API-to-storage pipeline.

    Pipeline:

        Mock API
            ↓
        Async HTTP client
            ↓
        Raw JSON
            ↓
        Pandas normalization
            ↓
        CSV / Parquet
            ↓
        Read back and validate
    """

    # =========================================================
    # 1. Mock API
    # =========================================================

    mock_users = create_mock_users()

    async def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        """Return mocked API data."""

        return httpx.Response(
            status_code=200,
            json=mock_users,
        )

    transport = httpx.MockTransport(handler)

    # =========================================================
    # 2. Fetch data through AsyncAPIClient
    # =========================================================

    async with httpx.AsyncClient(
        transport=transport,
    ) as mock_client:

        client = AsyncAPIClient(
            base_url="https://example.com",
            client=mock_client,
        )

        users = await client.fetch_users()

    # =========================================================
    # 3. Validate API response
    # =========================================================

    assert len(users) == 2

    assert users[0]["id"] == 101
    assert users[1]["id"] == 102

    assert users[0]["name"] == "Arun"
    assert users[1]["name"] == "Priya"

    # =========================================================
    # 4. Save raw JSON
    # =========================================================

    raw_file = (
        tmp_path
        / "raw"
        / "users.json"
    )

    save_json(
        users,
        raw_file,
    )

    assert raw_file.exists()

    # =========================================================
    # 5. Normalize API data
    # =========================================================

    customers_df = normalize_customers(
        users
    )

    addresses_df = normalize_addresses(
        users
    )

    companies_df = normalize_companies(
        users
    )

    # =========================================================
    # 6. Validate normalized datasets
    # =========================================================

    assert len(customers_df) == 2
    assert len(addresses_df) == 2
    assert len(companies_df) == 2

    # Customer dataset

    assert list(
        customers_df["customer_id"]
    ) == [101, 102]

    assert list(
        customers_df["name"]
    ) == ["Arun", "Priya"]

    assert list(
        customers_df["email"]
    ) == [
        "arun@example.com",
        "priya@example.com",
    ]

    # Address dataset

    assert list(
        addresses_df["customer_id"]
    ) == [101, 102]

    assert list(
        addresses_df["city"]
    ) == [
        "Chennai",
        "Coimbatore",
    ]

    # Company dataset

    assert list(
        companies_df["customer_id"]
    ) == [101, 102]

    assert list(
        companies_df["company_name"]
    ) == [
        "ABC Technologies",
        "XYZ Solutions",
    ]

    # =========================================================
    # 7. Save normalized datasets
    # =========================================================

    processed_dir = (
        tmp_path / "processed"
    )

    customers_csv = (
        processed_dir
        / "customers.csv"
    )

    customers_parquet = (
        processed_dir
        / "customers.parquet"
    )

    save_dataframe(
        customers_df,
        customers_csv,
    )

    save_dataframe(
        customers_df,
        customers_parquet,
    )

    # =========================================================
    # 8. Verify files were created
    # =========================================================

    assert customers_csv.exists()
    assert customers_parquet.exists()

    # =========================================================
    # 9. Read CSV and Parquet
    # =========================================================

    csv_result = pd.read_csv(
        customers_csv,
        dtype={
            "customer_id": "int64",
            "name": "string",
            "username": "string",
            "email": "string",
            "phone": "string",
            "website": "string",
        },
    )

    parquet_result = pd.read_parquet(
        customers_parquet,
    )

    # =========================================================
    # 10. Validate CSV contents
    # =========================================================

    assert len(csv_result) == len(
        customers_df
    )

    assert list(
        csv_result["customer_id"]
    ) == [101, 102]

    assert list(
        csv_result["name"]
    ) == ["Arun", "Priya"]

    assert list(
        csv_result["phone"]
    ) == [
        "1234567890",
        "9876543210",
    ]

    # =========================================================
    # 11. Validate Parquet contents
    # =========================================================

    assert len(parquet_result) == len(
        customers_df
    )

    assert list(
        parquet_result["customer_id"]
    ) == [101, 102]

    assert list(
        parquet_result["name"]
    ) == ["Arun", "Priya"]

    assert list(
        parquet_result["phone"]
    ) == [
        "1234567890",
        "9876543210",
    ]

    # =========================================================
    # 12. Validate column structure
    # =========================================================

    assert list(
        csv_result.columns
    ) == list(
        customers_df.columns
    )

    assert list(
        parquet_result.columns
    ) == list(
        customers_df.columns
    )