"""Generate synthetic customer transaction data."""
import argparse
import json
import random
from pathlib import Path


COUNTRIES = [
    "India",
    "USA",
    "UK",
    "Germany",
    "Singapore",
    "Australia",
    "Canada",
    "UAE",
]

FIRST_NAMES = [
    "Arun",
    "Priya",
    "Rahul",
    "Ananya",
    "Vikram",
    "Karthik",
    "Meera",
    "Aisha",
    "John",
    "David",
    "Sarah",
    "Emma",
]


def generate_customer(
    customer_id: int,
    min_transactions: int = 1,
    max_transactions: int = 10,
    min_transaction_value: int = 100,
    max_transaction_value: int = 5000,
) -> dict:
    """Generate a single synthetic customer."""

    transaction_count = random.randint(1, 5)

    transactions = [
    {
        "transaction_id": f"TXN-{customer_id}-{index:03d}",
        "amount": random.randint(100, 5000),
        "currency": "INR",
    }
    for index in range(1, transaction_count + 1)
]
    return {
        "id": customer_id,
        "name": random.choice(FIRST_NAMES),
        "country": random.choice(COUNTRIES),
        "transactions": transactions,
    }


def generate_customers(
    number_of_customers: int,
    duplicate_rate: float = 0.05,
    invalid_rate: float = 0.05,
) -> list[dict]:
    """Generate synthetic customer records."""

    customers = [
        generate_customer(customer_id)
        for customer_id in range(
            101,
            101 + number_of_customers,
        )
    ]

    duplicate_count = int(
        number_of_customers * duplicate_rate
    )

    if duplicate_count > 0:
        duplicate_customers = random.sample(
            customers,
            duplicate_count,
        )

        for customer in duplicate_customers:
            customers.append(customer.copy())

    invalid_count = int(
        number_of_customers * invalid_rate
    )

    for _ in range(invalid_count):
        customers.append(
            generate_invalid_customer()
        )

    random.shuffle(customers)

    return customers
def generate_invalid_customer() -> dict:
    """Generate an intentionally invalid customer record."""

    invalid_type = random.choice(
        [
            "missing_id",
            "invalid_id",
            "empty_transactions",
            "negative_transaction",
            "invalid_transaction_type",
        ]
    )

    customer = generate_customer(999999)

    if invalid_type == "missing_id":
        del customer["id"]

    elif invalid_type == "invalid_id":
        customer["id"] = "INVALID"

    elif invalid_type == "empty_transactions":
        customer["transactions"] = []

    elif invalid_type == "negative_transaction":
        customer["transactions"] = [-500, 1000]

    elif invalid_type == "invalid_transaction_type":
        customer["transactions"] = [1000, "INVALID"]

    return customer

def save_customers(
    customers: list[dict],
    output_file: Path,
) -> None:
    """Save customer data to a JSON file."""

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            customers,
            file,
            indent=4,
        )

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for data generation."""

    parser = argparse.ArgumentParser(
        description="Generate synthetic customer data."
    )

    parser.add_argument(
        "--customers",
        type=int,
        default=100,
        help="Number of customers to generate.",
    )

    parser.add_argument(
        "--duplicates",
        type=float,
        default=0.05,
        help="Duplicate customer rate.",
    )

    parser.add_argument(
        "--invalid",
        type=float,
        default=0.05,
        help="Invalid customer rate.",
    )

    return parser.parse_args()

def main() -> None:
    """Generate and save synthetic customer data."""

    random.seed(42)

    arguments = parse_arguments()

    output_file = (
        Path(__file__).parent.parent
        / "data"
        / "customers.json"
    )

    customers = generate_customers(
        number_of_customers=arguments.customers,
        duplicate_rate=arguments.duplicates,
        invalid_rate=arguments.invalid,
    )

    save_customers(
        customers,
        output_file,
    )

    print(
        f"Generated {len(customers)} customer records "
        f"and saved them to {output_file}"
    )