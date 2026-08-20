"""Application configuration."""

import os

from dotenv import load_dotenv


load_dotenv()


def get_api_base_url() -> str:
    """Return the configured API base URL."""

    base_url = os.getenv("API_BASE_URL")

    if not base_url:
        raise ValueError(
            "API_BASE_URL environment variable is not configured."
        )

    return base_url.rstrip("/")


def get_api_timeout() -> float:
    """Return the configured API timeout."""

    timeout = os.getenv(
        "API_TIMEOUT",
        "10",
    )

    try:
        return float(timeout)

    except ValueError as error:
        raise ValueError(
            "API_TIMEOUT must be a valid number."
        ) from error