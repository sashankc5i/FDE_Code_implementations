"""Application entry point."""

import asyncio

from api_pipeline.pipeline import run_pipeline


if __name__ == "__main__":
    asyncio.run(
        run_pipeline()
    )