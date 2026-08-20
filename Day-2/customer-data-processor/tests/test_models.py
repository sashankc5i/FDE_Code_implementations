"""Tests for the Customer and Transaction models."""

from customer_app.models import Customer, Transaction


def create_test_transactions() -> list[Transaction]:
    """Create reusable test transactions."""

    return [
        Transaction(
            transaction_id="TXN-101-001",
            amount=1200,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-002",
            amount=500,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-003",
            amount=800,
            currency="INR",
        ),
    ]


def test_transaction_creation():
    """Test that a Transaction object is created correctly."""

    transaction = Transaction(
        transaction_id="TXN-101-001",
        amount=1200,
        currency="INR",
    )

    assert transaction.transaction_id == "TXN-101-001"
    assert transaction.amount == 1200
    assert transaction.currency == "INR"


def test_customer_creation():
    """Test that a Customer object is created correctly."""

    transactions = create_test_transactions()

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=transactions,
    )

    assert customer.customer_id == 101
    assert customer.name == "Arun"
    assert customer.country == "India"
    assert customer.transactions == transactions


def test_total_spend():
    """Test total customer spending."""

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=create_test_transactions(),
    )

    assert customer.total_spend() == 2500


def test_average_transaction():
    """Test average transaction calculation."""

    transactions = [
        Transaction(
            transaction_id="TXN-101-001",
            amount=1000,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-002",
            amount=500,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-003",
            amount=500,
            currency="INR",
        ),
    ]

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=transactions,
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
        transactions=create_test_transactions(),
    )

    assert customer.is_high_value(2000) is True


def test_non_high_value_customer():
    """Test customer below the high-value threshold."""

    transactions = [
        Transaction(
            transaction_id="TXN-101-001",
            amount=500,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-002",
            amount=500,
            currency="INR",
        ),
        Transaction(
            transaction_id="TXN-101-003",
            amount=500,
            currency="INR",
        ),
    ]

    customer = Customer(
        customer_id=101,
        name="Arun",
        country="India",
        transactions=transactions,
    )

    assert customer.is_high_value(2000) is False