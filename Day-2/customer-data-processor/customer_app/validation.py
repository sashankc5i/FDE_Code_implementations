"""Validation functions for customer and transaction data."""

from customer_app.exceptions import InvalidCustomerDataError


def validate_transaction(transaction: dict) -> None:
    """
    Validate a single transaction dictionary.

    Raises:
        InvalidCustomerDataError:
            If the transaction data is invalid.
    """

    required_fields = {
        "transaction_id",
        "amount",
        "currency",
    }

    missing_fields = required_fields - transaction.keys()

    if missing_fields:
        raise InvalidCustomerDataError(
            f"Missing transaction fields: "
            f"{sorted(missing_fields)}"
        )

    if not isinstance(
        transaction["transaction_id"],
        str,
    ):
        raise InvalidCustomerDataError(
            "Transaction ID must be a string."
        )

    if not isinstance(
        transaction["amount"],
        (int, float),
    ):
        raise InvalidCustomerDataError(
            "Transaction amount must be an integer or float."
        )

    if transaction["amount"] < 0:
        raise InvalidCustomerDataError(
            "Transaction amount cannot be negative."
        )

    if not isinstance(
        transaction["currency"],
        str,
    ):
        raise InvalidCustomerDataError(
            "Transaction currency must be a string."
        )


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
            f"Missing required fields: "
            f"{sorted(missing_fields)}"
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

    for transaction in customer_data["transactions"]:

        if not isinstance(transaction, dict):
            raise InvalidCustomerDataError(
                "Every transaction must be a dictionary."
            )

        validate_transaction(transaction)