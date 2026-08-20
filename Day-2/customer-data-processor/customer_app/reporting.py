"""Reporting functions for customer data."""

from customer_app.models import Customer
from customer_app.processing import (
    calculate_average_transaction,
    find_duplicate_customer_ids,
    get_highest_transaction,
    get_high_value_customers,
    get_unique_countries,
)


def generate_summary(
    customers: list[Customer],
    high_value_threshold: float,
    invalid_customer_count: int = 0,
) -> dict:
    """Generate a summary of customer and transaction metrics."""

    high_value_customers = get_high_value_customers(
        customers,
        high_value_threshold,
    )

    return {
        "total_customers": len(customers),
        "invalid_customer_count": invalid_customer_count,
        "unique_countries": sorted(
            get_unique_countries(customers)
        ),
        "duplicate_customer_ids": find_duplicate_customer_ids(
            customers
        ),
        "high_value_customers": [
            customer.name
            for customer in high_value_customers
        ],
        "average_transaction": calculate_average_transaction(
            customers
        ),
        "highest_transaction": get_highest_transaction(
            customers
        ),
    }