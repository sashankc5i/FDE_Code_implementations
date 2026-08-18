"""Tests for reporting functions."""

from customer_app.models import Customer
from customer_app.reporting import generate_summary


def test_generate_summary():
    """Test the complete customer summary."""

    customers = [
        Customer(
            customer_id=101,
            name="Arun",
            country="India",
            transactions=[1200, 500, 800],
        ),
        Customer(
            customer_id=102,
            name="Priya",
            country="India",
            transactions=[2000, 1000],
        ),
        Customer(
            customer_id=103,
            name="John",
            country="USA",
            transactions=[500, 700, 300],
        ),
        Customer(
            customer_id=101,
            name="Arun",
            country="India",
            transactions=[1200, 500, 800],
        ),
    ]

    result = generate_summary(
        customers,
        high_value_threshold=2000,
    )

    assert result["total_customers"] == 4

    assert result["unique_countries"] == [
        "India",
        "USA",
    ]

    assert result["duplicate_customer_ids"] == [101]

    assert result["high_value_customers"] == [
        "Arun",
        "Priya",
        "Arun",
    ]

    assert result["average_transaction"] == 863.6363636363636

    assert result["highest_transaction"] == 2000