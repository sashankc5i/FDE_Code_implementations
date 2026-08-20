"""Tests for the application entry point."""

from pathlib import Path

from main import load_customer_data


def test_load_customer_data():
    """Test loading customer data from JSON."""

    data_file = (
        Path(__file__).parent.parent
        / "data"
        / "customers.json"
    )

    data = load_customer_data(data_file)

    assert isinstance(data, list)
    assert len(data) > 0

    assert "id" in data[0]
    assert "name" in data[0]
    assert "country" in data[0]
    assert "transactions" in data[0]
import pytest

from customer_app.exceptions import InvalidCustomerDataError
from customer_app.validation import validate_customer_data


def test_invalid_customer_can_be_identified():
    """Invalid records should raise a known exception."""

    invalid_customer = {
        "id": "INVALID",
        "name": "Arun",
        "country": "India",
        "transactions": [1000],
    }

    with pytest.raises(InvalidCustomerDataError):
        validate_customer_data(invalid_customer)