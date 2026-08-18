"""Tests for the Customer model."""

from customer_app.models import Customer


def test_customer_creation():
    """Test that a Customer object is created correctly."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[1200, 500, 800],
    )

    assert customer.customer_id == 101
    assert customer.name == "Arun"
    assert customer.country == "India"
    assert customer.transactions == [1200, 500, 800]


def test_total_spend():
    """Test total customer spending."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[1200, 500, 800],
    )

    assert customer.total_spend() == 2500


def test_average_transaction():
    """Test average transaction calculation."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[1000, 500, 500],
    )

    assert customer.average_transaction() == 666.6666666666666


def test_average_transaction_with_no_transactions():
    """Test average transaction when no transactions exist."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[],
    )

    assert customer.average_transaction() == 0.0


def test_high_value_customer():
    """Test high-value customer detection."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[1200, 500, 800],
    )

    assert customer.is_high_value(2000) is True


def test_non_high_value_customer():
    """Test customer below the high-value threshold."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=[500, 500, 500],
    )

    assert customer.is_high_value(2000) is False