"""Demonstrate concurrent asynchronous API requests."""

import asyncio
import time

import httpx


URLS = [
    "https://jsonplaceholder.typicode.com/users",
    "https://jsonplaceholder.typicode.com/posts",
    "https://jsonplaceholder.typicode.com/todos",
]


async def fetch(
    client: httpx.AsyncClient,
    url: str,
) -> dict:
    """Fetch one URL asynchronously."""

    response = await client.get(url)

    response.raise_for_status()

    return {
        "url": url,
        "records": len(response.json()),
    }


async def fetch_all() -> list[dict]:
    """Fetch all endpoints concurrently."""

    async with httpx.AsyncClient(
        timeout=10,
    ) as client:

        tasks = [
            fetch(client, url)
            for url in URLS
        ]

        return await asyncio.gather(*tasks)


async def main() -> None:
    """Run the asynchronous demonstration."""

    start = time.perf_counter()

    results = await fetch_all()

    elapsed = time.perf_counter() - start

    for result in results:
        print(
            f"{result['url']} "
            f"→ {result['records']} records"
        )

    print(
        f"\nCompleted in {elapsed:.2f} seconds."
    )


if __name__ == "__main__":
    asyncio.run(main())