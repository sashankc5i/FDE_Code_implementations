"""Application entry point."""

import argparse
import json
from pathlib import Path

from customer_app.service import process_customer_data

def parse_arguments() -> argparse.Namespace:
    """Parse application command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Process customer transaction data."
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=2000,
        help="High-value customer spending threshold.",
    )

    return parser.parse_args()

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "customers.json"
)


def load_customer_data(
    file_path: Path,
) -> list[dict]:
    """Load customer data from a JSON file."""

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def print_report(summary: dict) -> None:
    """Print the customer data quality report."""

    print("\n=== Customer Data Quality Report ===")

    print(
        f"Total customers: "
        f"{summary['total_customers']}"
    )

    print(
        f"Invalid customer records: "
        f"{summary['invalid_customer_count']}"
    )

    print(
        f"Unique countries: "
        f"{summary['unique_countries']}"
    )

    print(
        f"Duplicate customer IDs: "
        f"{summary['duplicate_customer_ids']}"
    )

    print(
        f"High-value customers: "
        f"{summary['high_value_customers']}"
    )

    print(
        f"Average transaction: "
        f"{summary['average_transaction']:.2f}"
    )

    print(
        f"Highest transaction: "
        f"{summary['highest_transaction']:.2f}"
    )


def main() -> None:
    """Run the customer data processing application."""

    arguments = parse_arguments()

    raw_customers = load_customer_data(DATA_FILE)

    summary = process_customer_data(
        raw_customers,
        high_value_threshold=arguments.threshold,
    )

    print_report(summary)


if __name__ == "__main__":
    main()