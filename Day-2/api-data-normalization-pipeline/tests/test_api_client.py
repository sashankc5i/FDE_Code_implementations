"""Tests for the API client."""

import httpx

from api_pipeline.api_client import APIClient
import pytest

def test_fetch_users_success():
    """Successful API response should return user data."""

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 1,
                    "name": "Arun",
                }
            ],
        )

    mock_client = httpx.Client(
        transport=httpx.MockTransport(handler),
    )

    client = APIClient(
        base_url="https://example.com",
        client=mock_client,
    )

    users = client.fetch_users()

    assert len(users) == 1
    assert users[0]["id"] == 1

    mock_client.close()
def test_fetch_users_http_error():
    """HTTP errors should be raised."""

    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            json={
                "error": "Internal server error"
            },
        )

    mock_client = httpx.Client(
        transport=httpx.MockTransport(handler),
    )

    client = APIClient(
        base_url="https://example.com",
        client=mock_client,
    )

    try:
        with pytest.raises(
            httpx.HTTPStatusError
        ):
            client.fetch_users()
    finally:
        mock_client.close()