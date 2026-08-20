"""Tests for the asynchronous API client."""

import httpx
import pytest

from api_pipeline.api_client import AsyncAPIClient


@pytest.mark.asyncio
async def test_fetch_users_success():
    """Successful async API response should return user data."""

    async def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json=[
                {
                    "id": 101,
                    "name": "Arun",
                }
            ],
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        transport=transport,
    ) as mock_client:

        client = AsyncAPIClient(
            base_url="https://example.com",
            client=mock_client,
        )

        users = await client.fetch_users()

    assert len(users) == 1
    assert users[0]["id"] == 101
    assert users[0]["name"] == "Arun"