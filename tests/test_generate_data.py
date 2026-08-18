"""Tests for synthetic customer data generation."""

from pathlib import Path

from scripts.generate_data import (
    generate_customer,
    generate_customers,
    save_customers,
)


def test_generate_customer():
    """Test that a single customer has the expected structure."""

    customer = generate_customer(101)

    assert customer["id"] == 101
    assert isinstance(customer["name"], str)
    assert isinstance(customer["country"], str)
    assert isinstance(customer["transactions"], list)

    assert len(customer["transactions"]) >= 1


def test_generate_customer_transaction_range():
    """Test that generated transactions stay within the configured range."""

    customer = generate_customer(
        customer_id=101,
        min_transactions=5,
        max_transactions=5,
        min_transaction_value=100,
        max_transaction_value=500,
    )

    assert len(customer["transactions"]) == 5

    assert all(
        100 <= transaction <= 500
        for transaction in customer["transactions"]
    )


def test_generate_customers():
    """Test generating customers without duplicates."""

    customers = generate_customers(
        number_of_customers=10,
        duplicate_rate=0,
    )

    assert len(customers) == 10

    customer_ids = [
        customer["id"]
        for customer in customers
    ]

    assert len(set(customer_ids)) == 10


def test_generate_customers_with_duplicates():
    """Test that the configured duplicate rate creates duplicates."""

    customers = generate_customers(
        number_of_customers=100,
        duplicate_rate=0.10,
        invalid_rate=0,
    )

    assert len(customers) == 110


def test_save_customers(tmp_path):
    """Test that customer data can be saved as JSON."""

    output_file = tmp_path / "customers.json"

    customers = generate_customers(
        number_of_customers=5,
        duplicate_rate=0,
    )

    save_customers(
        customers,
        output_file,
    )

    assert output_file.exists()
def test_generate_invalid_customer():
    """Test that an invalid customer is generated."""

    from scripts.generate_data import generate_invalid_customer

    customer = generate_invalid_customer()

    assert isinstance(customer, dict)