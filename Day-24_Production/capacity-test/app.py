import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/chat")
async def chat():
    start = time.perf_counter()

    # Simulate an AI/model call.
    await asyncio.sleep(1)

    latency = time.perf_counter() - start

    return {
        "response": "AI response",
        "latency": latency
    }