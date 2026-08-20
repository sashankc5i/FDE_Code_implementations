"""Tests for customer data processing functions."""

from customer_app.models import Customer, Transaction
from customer_app.processing import (
    calculate_average_transaction,
    create_customers,
    find_duplicate_customer_ids,
    get_all_transactions,
    get_highest_transaction,
    get_high_value_customers,
    get_unique_countries,
)


def create_test_transactions(
    amounts: list[float],
    customer_id: int,
) -> list[Transaction]:
    """Create Transaction objects for testing."""

    return [
        Transaction(
            transaction_id=f"TXN-{customer_id}-{index:03d}",
            amount=amount,
            currency="INR",
        )
        for index, amount in enumerate(amounts, start=1)
    ]


def create_test_customers() -> list[Customer]:
    """Create reusable Customer objects for testing."""

    return [
        Customer(
            customer_id=101,
            name="Arun",
            country="India",
            transactions=create_test_transactions(
                [1200, 500, 800],
                customer_id=101,
            ),
        ),
        Customer(
            customer_id=102,
            name="Priya",
            country="India",
            transactions=create_test_transactions(
                [2000, 1000],
                customer_id=102,
            ),
        ),
        Customer(
            customer_id=103,
            name="John",
            country="USA",
            transactions=create_test_transactions(
                [500, 700, 300],
                customer_id=103,
            ),
        ),
        Customer(
            customer_id=101,
            name="Arun",
            country="India",
            transactions=create_test_transactions(
                [1200, 500, 800],
                customer_id=101,
            ),
        ),
    ]


def test_create_customers():
    """Test conversion from dictionaries to Customer objects."""

    raw_data = [
        {
            "id": 101,
            "name": "Arun",
            "country": "India",
            "transactions": [
                {
                    "transaction_id": "TXN-101-001",
                    "amount": 1200,
                    "currency": "INR",
                },
                {
                    "transaction_id": "TXN-101-002",
                    "amount": 500,
                    "currency": "INR",
                },
                {
                    "transaction_id": "TXN-101-003",
                    "amount": 800,
                    "currency": "INR",
                },
            ],
        }
    ]

    customers = create_customers(raw_data)

    assert len(customers) == 1

    customer = customers[0]

    assert customer.customer_id == 101
    assert customer.name == "Arun"
    assert customer.country == "India"

    assert len(customer.transactions) == 3

    assert customer.transactions[0].transaction_id == "TXN-101-001"
    assert customer.transactions[0].amount == 1200
    assert customer.transactions[0].currency == "INR"


def test_get_high_value_customers():
    """Test identification of high-value customers."""

    customers = create_test_customers()

    result = get_high_value_customers(
        customers,
        threshold=2000,
    )

    assert len(result) == 3

    assert [customer.customer_id for customer in result] == [
        101,
        102,
        101,
    ]


def test_get_unique_countries():
    """Test extraction of unique customer countries."""

    customers = create_test_customers()

    result = get_unique_countries(customers)

    assert result == {"India", "USA"}


def test_find_duplicate_customer_ids():
    """Test detection of duplicate customer IDs."""

    customers = create_test_customers()

    result = find_duplicate_customer_ids(customers)

    assert result == [101]


def test_get_all_transactions():
    """Test flattening customer transactions."""

    customers = create_test_customers()

    result = get_all_transactions(customers)

    assert len(result) == 11

    assert result[0].amount == 1200
    assert result[1].amount == 500
    assert result[2].amount == 800


def test_calculate_average_transaction():
    """Test average transaction calculation."""

    customers = create_test_customers()

    result = calculate_average_transaction(customers)

    # Total = 9500
    # Number of transactions = 11
    # Average = 863.6363...
    assert round(result, 2) == 863.64


def test_get_highest_transaction():
    """Test highest transaction calculation."""

    customers = create_test_customers()

    result = get_highest_transaction(customers)

    assert result == 2000


def test_calculate_average_transaction_with_no_customers():
    """Average should be zero when there are no customers."""

    result = calculate_average_transaction([])

    assert result == 0.0


def test_highest_transaction_with_no_customers():
    """Highest transaction should be zero when there are no customers."""

    result = get_highest_transaction([])

    assert result == 0.0


def test_get_high_value_customers_with_no_customers():
    """No customers should return an empty list."""

    result = get_high_value_customers([])

    assert result == []


def test_get_unique_countries_with_no_customers():
    """No customers should return an empty set."""

    result = get_unique_countries([])

    assert result == set()


def test_find_duplicate_customer_ids_with_no_customers():
    """No customers should have no duplicate IDs."""

    result = find_duplicate_customer_ids([])

    assert result == []


def test_get_all_transactions_with_no_customers():
    """No customers should return an empty transaction list."""

    result = get_all_transactions([])

    assert result == []