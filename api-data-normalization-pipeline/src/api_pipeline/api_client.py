"""HTTP clients for external APIs."""

import asyncio

import httpx


class APIClient:
    """Synchronous client for external APIs."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        client: httpx.Client | None = None,
    ) -> None:
        """Initialize the synchronous API client."""

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = client

    def fetch_users(self) -> list[dict]:
        """Fetch users from the API."""

        url = f"{self.base_url}/users"

        if self.client is not None:
            response = self.client.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        with httpx.Client(
            timeout=self.timeout,
        ) as client:

            response = client.get(url)

            response.raise_for_status()

            return response.json()


class AsyncAPIClient:
    """Asynchronous client for external APIs."""

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        max_retries: int = 3,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """Initialize the asynchronous API client."""

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = client

    async def fetch_users(self) -> list[dict]:
        """Fetch users asynchronously."""

        return await self._fetch_with_retry(
            "/users"
        )

    async def _fetch_with_retry(
        self,
        endpoint: str,
    ) -> list[dict]:
        """
        Fetch an endpoint with retry handling.

        Retries transient network failures using
        exponential backoff.
        """

        url = (
            f"{self.base_url}/"
            f"{endpoint.lstrip('/')}"
        )

        for attempt in range(
            self.max_retries + 1
        ):
            try:

                if self.client is not None:
                    response = await self.client.get(
                        url,
                        timeout=self.timeout,
                    )

                    response.raise_for_status()

                    return response.json()

                async with httpx.AsyncClient(
                    timeout=self.timeout,
                ) as client:

                    response = await client.get(
                        url
                    )

                    response.raise_for_status()

                    return response.json()

            except (
                httpx.TimeoutException,
                httpx.ConnectError,
                httpx.ReadError,
            ):

                if attempt >= self.max_retries:
                    raise

                await asyncio.sleep(
                    2 ** attempt
                )

        raise RuntimeError(
            "Request failed unexpectedly."
        )

    async def fetch(
        self,
        client: httpx.AsyncClient,
        endpoint: str,
    ) -> list[dict]:
        """
        Fetch data from an API endpoint.

        Args:
            client: Shared async HTTP client.
            endpoint: API endpoint path.

        Returns:
            JSON response as a list of dictionaries.
        """

        url = (
            f"{self.base_url}/"
            f"{endpoint.lstrip('/')}"
        )

        response = await client.get(
            url,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    async def fetch_multiple(
        self,
        endpoints: list[str],
    ) -> dict[str, list[dict]]:
        """
        Fetch multiple endpoints concurrently.

        Args:
            endpoints: API endpoint paths.

        Returns:
            Dictionary mapping endpoint names
            to API responses.
        """

        async with httpx.AsyncClient(
            timeout=self.timeout,
        ) as client:

            tasks = [
                self.fetch(
                    client,
                    endpoint,
                )
                for endpoint in endpoints
            ]

            responses = await asyncio.gather(
                *tasks
            )

        return dict(
            zip(
                endpoints,
                responses,
            )
        )