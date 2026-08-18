"""Business processing functions for customer data."""

from collections import Counter

from customer_app.models import Customer


def create_customers(
    customer_data: list[dict],
) -> list[Customer]:
    """Convert raw dictionaries into Customer objects."""

    return [
        Customer(
            customer_id=data["id"],
            name=data["name"],
            country=data["country"],
            transactions=data["transactions"],
        )
        for data in customer_data
    ]


def get_high_value_customers(
    customers: list[Customer],
    threshold: float,
) -> list[Customer]:
    """Return customers whose total spending exceeds the threshold."""

    return [
        customer
        for customer in customers
        if customer.is_high_value(threshold)
    ]


def get_unique_countries(
    customers: list[Customer],
) -> set[str]:
    """Return the unique countries represented by customers."""

    return {
        customer.country
        for customer in customers
    }


def find_duplicate_customer_ids(
    customers: list[Customer],
) -> list[int]:
    """Return customer IDs that appear more than once."""

    id_counts = Counter(
        customer.customer_id
        for customer in customers
    )

    return [
        customer_id
        for customer_id, count in id_counts.items()
        if count > 1
    ]


def get_all_transactions(
    customers: list[Customer],
) -> list[float]:
    """Return all transactions across all customers."""

    return [
        transaction
        for customer in customers
        for transaction in customer.transactions
    ]


def calculate_average_transaction(
    customers: list[Customer],
) -> float:
    """Calculate the average transaction value."""

    transactions = get_all_transactions(customers)

    if not transactions:
        return 0.0

    return sum(transactions) / len(transactions)


def get_highest_transaction(
    customers: list[Customer],
) -> float:
    """Return the highest transaction value."""

    transactions = get_all_transactions(customers)

    if not transactions:
        return 0.0

    return max(transactions)