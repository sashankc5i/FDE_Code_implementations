"""Tests for customer processing functions."""

from customer_app.models import Customer
from customer_app.processing import (
    calculate_average_transaction,
    create_customers,
    find_duplicate_customer_ids,
    get_all_transactions,
    get_highest_transaction,
    get_high_value_customers,
    get_unique_countries,
)


def create_test_customers() -> list[Customer]:
    """Create reusable customers for testing."""

    return [
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


def test_create_customers():
    """Test conversion from dictionaries to Customer objects."""

    raw_data = [
        {
            "id": 101,
            "name": "Arun",
            "country": "India",
            "transactions": [1200, 500, 800],
        }
    ]

    customers = create_customers(raw_data)

    assert len(customers) == 1
    assert isinstance(customers[0], Customer)
    assert customers[0].customer_id == 101
    assert customers[0].name == "Arun"


def test_get_high_value_customers():
    """Test identification of high-value customers."""

    customers = create_test_customers()

    result = get_high_value_customers(
        customers,
        threshold=2000,
    )

    assert len(result) == 3


def test_get_unique_countries():
    """Test extraction of unique countries."""

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
    assert 2000 in result


def test_calculate_average_transaction():
    """Test average transaction calculation."""

    customers = create_test_customers()

    result = calculate_average_transaction(customers)

    assert round(result, 2) == 863.64


def test_get_highest_transaction():
    """Test highest transaction calculation."""

    customers = create_test_customers()

    result = get_highest_transaction(customers)

    assert result == 2000
   
def test_average_transaction_with_no_customers():
    """Average should be zero when there are no customers."""

    result = calculate_average_transaction([])

    assert result == 0.0
def test_highest_transaction_with_no_customers():
    """Highest transaction should be zero when there are no customers."""

    result = get_highest_transaction([])

    assert result == 0.0