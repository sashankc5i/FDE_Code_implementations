"""Tests for the application service layer."""

from customer_app.service import process_customer_data


def test_process_customer_data_with_valid_records():
    """Valid records should be processed successfully."""

    customers = [
        {
            "id": 101,
            "name": "Arun",
            "country": "India",
            "transactions": [1200, 500, 800],
        },
        {
            "id": 102,
            "name": "Priya",
            "country": "India",
            "transactions": [2000, 1000],
        },
    ]

    result = process_customer_data(customers)

    assert result["total_customers"] == 2
    assert result["invalid_customer_count"] == 0
    assert result["high_value_customers"] == [
        "Arun",
        "Priya",
    ]


def test_process_customer_data_with_invalid_record():
    """Invalid records should be excluded and counted."""

    customers = [
        {
            "id": 101,
            "name": "Arun",
            "country": "India",
            "transactions": [1200, 500, 800],
        },
        {
            "id": "INVALID",
            "name": "Bad Customer",
            "country": "India",
            "transactions": [1000],
        },
    ]

    result = process_customer_data(customers)

    assert result["total_customers"] == 1
    assert result["invalid_customer_count"] == 1