"""Validation functions for customer data."""

from customer_app.exceptions import InvalidCustomerDataError
def validate_customer_data(customer_data: dict) -> None:
    """
    Validate a raw customer dictionary.

    Raises:
        InvalidCustomerDataError:
            If the customer data is invalid.
    """

    required_fields = {
        "id",
        "name",
        "country",
        "transactions",
    }

    missing_fields = required_fields - customer_data.keys()

    if missing_fields:
        raise InvalidCustomerDataError(
            f"Missing required fields: {sorted(missing_fields)}"
        )

    if not isinstance(customer_data["id"], int):
        raise InvalidCustomerDataError(
            "Customer ID must be an integer."
        )

    if not isinstance(customer_data["name"], str):
        raise InvalidCustomerDataError(
            "Customer name must be a string."
        )

    if not isinstance(customer_data["country"], str):
        raise InvalidCustomerDataError(
            "Customer country must be a string."
        )

    if not isinstance(customer_data["transactions"], list):
        raise InvalidCustomerDataError(
            "Transactions must be a list."
        )

    if not customer_data["transactions"]:
        raise InvalidCustomerDataError(
            "Transactions cannot be empty."
        )

    if not all(
        isinstance(transaction, (int, float))
        for transaction in customer_data["transactions"]
    ):
        raise InvalidCustomerDataError(
            "Every transaction must be an integer or float."
        )

    if any(
        transaction < 0
        for transaction in customer_data["transactions"]
    ):
        raise InvalidCustomerDataError(
            "Transaction values cannot be negative."
        )