"""Business processing functions for customer data."""

from collections import Counter

from customer_app.models import Customer, Transaction


def create_customers(
    customer_data: list[dict],
) -> list[Customer]:
    """
    Convert raw customer dictionaries into Customer objects.

    Args:
        customer_data: Raw customer records.

    Returns:
        A list of Customer objects.
    """

    customers = []

    for data in customer_data:
        transactions = [
            Transaction(
                transaction_id=transaction["transaction_id"],
                amount=transaction["amount"],
                currency=transaction["currency"],
            )
            for transaction in data["transactions"]
        ]

        customer = Customer(
            customer_id=data["id"],
            name=data["name"],
            country=data["country"],
            transactions=transactions,
        )

        customers.append(customer)

    return customers


def get_high_value_customers(
    customers: list[Customer],
    threshold: float = 2000,
) -> list[Customer]:
    """
    Return customers whose total spending exceeds the threshold.

    Args:
        customers: Customer objects.
        threshold: Minimum spending required to be high value.

    Returns:
        Customers whose total spend is greater than the threshold.
    """

    return [
        customer
        for customer in customers
        if customer.is_high_value(threshold)
    ]


def get_unique_countries(
    customers: list[Customer],
) -> set[str]:
    """
    Return the unique countries represented by customers.

    Args:
        customers: Customer objects.

    Returns:
        A set containing unique countries.
    """

    return {
        customer.country
        for customer in customers
    }


def find_duplicate_customer_ids(
    customers: list[Customer],
) -> list[int]:
    """
    Find customer IDs that occur more than once.

    Args:
        customers: Customer objects.

    Returns:
        Sorted list of duplicate customer IDs.
    """

    customer_id_counts = Counter(
        customer.customer_id
        for customer in customers
    )

    return sorted(
        customer_id
        for customer_id, count in customer_id_counts.items()
        if count > 1
    )


def get_all_transactions(
    customers: list[Customer],
) -> list[Transaction]:
    """
    Flatten transactions from all customers.

    Args:
        customers: Customer objects.

    Returns:
        A list containing every Transaction object.
    """

    return [
        transaction
        for customer in customers
        for transaction in customer.transactions
    ]


def calculate_average_transaction(
    customers: list[Customer],
) -> float:
    """
    Calculate the average transaction amount.

    Args:
        customers: Customer objects.

    Returns:
        Average transaction amount, or 0.0 if there are no transactions.
    """

    transactions = get_all_transactions(customers)

    if not transactions:
        return 0.0

    return sum(
        transaction.amount
        for transaction in transactions
    ) / len(transactions)


def get_highest_transaction(
    customers: list[Customer],
) -> float:
    """
    Return the highest transaction amount.

    Args:
        customers: Customer objects.

    Returns:
        Highest transaction amount, or 0.0 if there are no transactions.
    """

    transactions = get_all_transactions(customers)

    if not transactions:
        return 0.0

    return max(
        transaction.amount
        for transaction in transactions
    )