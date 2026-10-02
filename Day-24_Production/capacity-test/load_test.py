import asyncio
import statistics
import time

import httpx


URL = "http://localhost:8000/chat"


async def send_request(client):
    start = time.perf_counter()

    try:
        response = await client.post(URL, timeout=30)

        latency = time.perf_counter() - start

        return {
            "success": response.status_code == 200,
            "latency": latency,
            "status": response.status_code,
        }

    except Exception:
        return {
            "success": False,
            "latency": None,
            "status": None,
        }


async def run_test(concurrency):
    async with httpx.AsyncClient() as client:

        start = time.perf_counter()

        tasks = [
            send_request(client)
            for _ in range(concurrency)
        ]

        results = await asyncio.gather(*tasks)

        duration = time.perf_counter() - start

    successful = [
        r for r in results
        if r["success"]
    ]

    latencies = [
        r["latency"]
        for r in successful
    ]

    success_rate = (
        len(successful) / len(results)
    ) * 100

    throughput = len(results) / duration

    p50 = statistics.median(latencies)

    print(
        f"\nConcurrency: {concurrency}"
    )

    print(
        f"Requests: {len(results)}"
    )

    print(
        f"Success rate: {success_rate:.2f}%"
    )

    print(
        f"Throughput: {throughput:.2f} req/sec"
    )

    print(
        f"p50 latency: {p50:.2f}s"
    )


async def main():

    for concurrency in [1, 5, 10, 25, 50, 100]:

        await run_test(concurrency)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())