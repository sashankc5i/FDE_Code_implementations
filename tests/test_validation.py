"""Tests for customer data validation."""

import pytest

from customer_app.exceptions import InvalidCustomerDataError
from customer_app.validation import validate_customer_data


def test_valid_customer_data():
    """Valid customer data should pass validation."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
        "transactions": [1200, 500, 800],
    }

    validate_customer_data(customer)


def test_missing_required_field():
    """Missing fields should raise an exception."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_invalid_customer_id():
    """Customer ID must be an integer."""

    customer = {
        "id": "101",
        "name": "Arun",
        "country": "India",
        "transactions": [1200, 500],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_invalid_name():
    """Customer name must be a string."""

    customer = {
        "id": 101,
        "name": 123,
        "country": "India",
        "transactions": [1200, 500],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_invalid_country():
    """Customer country must be a string."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": 123,
        "transactions": [1200, 500],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_transactions_must_be_list():
    """Transactions must be provided as a list."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
        "transactions": 1000,
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_empty_transactions():
    """An empty transaction list should be rejected."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
        "transactions": [],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_invalid_transaction_type():
    """Transactions must contain numbers."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
        "transactions": [1000, "INVALID"],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)


def test_negative_transaction():
    """Negative transaction values should be rejected."""

    customer = {
        "id": 101,
        "name": "Arun",
        "country": "India",
        "transactions": [1000, -500],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(customer)