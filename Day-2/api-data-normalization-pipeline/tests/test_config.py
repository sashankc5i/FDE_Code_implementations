"""Tests for application configuration."""

import pytest

from api_pipeline.config import (
    get_api_base_url,
    get_api_timeout,
)


def test_get_api_base_url(monkeypatch):
    """API base URL should be loaded from environment."""

    monkeypatch.setenv(
        "API_BASE_URL",
        "https://example.com/",
    )

    result = get_api_base_url()

    assert result == "https://example.com"


def test_get_api_base_url_missing(monkeypatch):
    """Missing API base URL should raise an error."""

    monkeypatch.delenv(
        "API_BASE_URL",
        raising=False,
    )

    with pytest.raises(
        ValueError,
        match="API_BASE_URL",
    ):
        get_api_base_url()


def test_get_api_timeout(monkeypatch):
    """API timeout should be converted to float."""

    monkeypatch.setenv(
        "API_TIMEOUT",
        "15",
    )

    result = get_api_timeout()

    assert result == 15.0


def test_get_api_timeout_invalid(monkeypatch):
    """Invalid API timeout should raise an error."""

    monkeypatch.setenv(
        "API_TIMEOUT",
        "invalid",
    )

    with pytest.raises(
        ValueError,
        match="API_TIMEOUT",
    ):
        get_api_timeout()