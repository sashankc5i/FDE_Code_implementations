"""Application service layer."""

from customer_app.exceptions import InvalidCustomerDataError
from customer_app.processing import create_customers
from customer_app.reporting import generate_summary
from customer_app.validation import validate_customer_data


def process_customer_data(
    raw_customers: list[dict],
    high_value_threshold: float = 2000,
) -> dict:
    """
    Validate and process customer data.

    Invalid records are excluded from processing and
    included in the final summary.
    """

    valid_customer_data = []
    invalid_customer_data = []

    for customer_data in raw_customers:
        try:
            validate_customer_data(customer_data)
            valid_customer_data.append(customer_data)

        except InvalidCustomerDataError as error:
            invalid_customer_data.append(
                {
                    "data": customer_data,
                    "error": str(error),
                }
            )

    customers = create_customers(valid_customer_data)

    summary = generate_summary(
        customers,
        high_value_threshold=high_value_threshold,
        invalid_customer_count=len(invalid_customer_data),
    )

    return summary