"""Tests for API data normalization."""

import pandas as pd

from api_pipeline.normalization import (
    normalize_addresses,
    normalize_companies,
    normalize_customers,
)


def create_test_users() -> list[dict]:
    """Create sample API user data for testing."""

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
def test_normalize_customers():
    """Customer data should be normalized correctly."""

    users = create_test_users()

    result = normalize_customers(users)

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 2

    assert list(result.columns) == [
        "customer_id",
        "name",
        "username",
        "email",
        "phone",
        "website",
    ]

    assert result.iloc[0]["customer_id"] == 101
    assert result.iloc[0]["name"] == "Arun"
    assert result.iloc[1]["customer_id"] == 102
    assert result.iloc[1]["name"] == "Priya"
def test_normalize_addresses():
    """Address data should be normalized correctly."""

    users = create_test_users()

    result = normalize_addresses(users)

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 2

    assert list(result.columns) == [
        "customer_id",
        "street",
        "suite",
        "city",
        "zipcode",
        "latitude",
        "longitude",
    ]

    assert result.iloc[0]["customer_id"] == 101
    assert result.iloc[0]["city"] == "Chennai"
    assert result.iloc[0]["latitude"] == "13.0827"
    assert result.iloc[0]["longitude"] == "80.2707"
def test_normalize_companies():
    """Company data should be normalized correctly."""

    users = create_test_users()

    result = normalize_companies(users)

    assert isinstance(result, pd.DataFrame)

    assert len(result) == 2

    assert list(result.columns) == [
        "customer_id",
        "company_name",
        "catch_phrase",
        "business_description",
    ]

    assert result.iloc[0]["customer_id"] == 101
    assert result.iloc[0]["company_name"] == (
        "ABC Technologies"
    )

    assert result.iloc[1]["company_name"] == (
        "XYZ Solutions"
    )
def test_normalize_empty_users():
    """Empty API response should produce empty DataFrames."""

    customers = normalize_customers([])
    addresses = normalize_addresses([])
    companies = normalize_companies([])

    assert isinstance(customers, pd.DataFrame)
    assert isinstance(addresses, pd.DataFrame)
    assert isinstance(companies, pd.DataFrame)

    assert customers.empty
    assert addresses.empty
    assert companies.empty