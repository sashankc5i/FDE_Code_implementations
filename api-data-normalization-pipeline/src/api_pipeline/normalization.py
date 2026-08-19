"""Functions for normalizing API data."""

import pandas as pd


def normalize_customers(
    users: list[dict],
) -> pd.DataFrame:
    """
    Create the customer dataset from raw user data.

    Args:
        users: Raw API user dictionaries.

    Returns:
        Customer DataFrame.
    """

    return pd.DataFrame(
        [
            {
                "customer_id": user["id"],
                "name": user["name"],
                "username": user["username"],
                "email": user["email"],
                "phone": user["phone"],
                "website": user["website"],
            }
            for user in users
        ]
    )


def normalize_addresses(
    users: list[dict],
) -> pd.DataFrame:
    """
    Create the address dataset from raw user data.

    Args:
        users: Raw API user dictionaries.

    Returns:
        Address DataFrame.
    """

    return pd.DataFrame(
        [
            {
                "customer_id": user["id"],
                "street": user["address"]["street"],
                "suite": user["address"]["suite"],
                "city": user["address"]["city"],
                "zipcode": user["address"]["zipcode"],
                "latitude": user["address"]["geo"]["lat"],
                "longitude": user["address"]["geo"]["lng"],
            }
            for user in users
        ]
    )


def normalize_companies(
    users: list[dict],
) -> pd.DataFrame:
    """
    Create the company dataset from raw user data.

    Args:
        users: Raw API user dictionaries.

    Returns:
        Company DataFrame.
    """

    return pd.DataFrame(
        [
            {
                "customer_id": user["id"],
                "company_name": user["company"]["name"],
                "catch_phrase": user["company"]["catchPhrase"],
                "business_description": user["company"]["bs"],
            }
            for user in users
        ]
    )