from fastapi import FastAPI

from simulator import ModelSimulator
from reliability import retry_with_backoff, CircuitBreaker


app = FastAPI(title="AI Reliability Lab")

model = ModelSimulator()

primary_circuit = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=1.0,
)


async def call_primary():
    return await retry_with_backoff(
        operation=lambda: model.call("primary-model"),
        max_retries=3,
        base_delay=0.1,
        jitter=0.05,
        circuit_breaker=primary_circuit,
    )


async def call_fallback():
    result = await model.call("fallback-model")

    return {
        "success": True,
        "model": result["model"],
        "response": result["response"],
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "primary_circuit": primary_circuit.state.value,
    }


@app.post("/failure-mode/{mode}")
async def set_failure_mode(mode: str):

    model.set_failure_mode(mode)

    return {
        "failure_mode": mode
    }


@app.get("/chat")
async def chat():

    # 1. Try primary
    primary_result = await call_primary()

    if primary_result["success"]:

        return {
            "status": "success",
            "model": primary_result["result"]["model"],
            "response": primary_result["result"]["response"],
            "service_mode": "primary",
            "circuit_state": primary_result["circuit_state"],
            "retry_count": primary_result["retry_count"],
        }

    # 2. Primary failed → fallback
    try:

        fallback_result = await call_fallback()

        return {
            "status": "degraded_success",
            "model": fallback_result["model"],
            "response": fallback_result["response"],
            "service_mode": "fallback",
            "primary_error": primary_result["error"],
            "circuit_state": primary_result.get(
                "circuit_state"
            ),
        }

    except Exception as exc:

        return {
            "status": "failure",
            "error": str(exc),
            "service_mode": "unavailable",
        }