from fastapi import FastAPI

from cost_model import (
    InfrastructureCost,
    RequestCost,
    calculate_request_cost,
    calculate_monthly_cost,
)

from simulator import (
    LARGE_MODEL,
    DEFAULT_INPUT_TOKENS,
    DEFAULT_OUTPUT_TOKENS,
)

from optimizer import run_optimization


app = FastAPI(
    title="AI Cost & FinOps Lab"
)


infrastructure = InfrastructureCost()


@app.get("/cost/baseline")
async def baseline():

    request = RequestCost(
        input_tokens=DEFAULT_INPUT_TOKENS,
        output_tokens=DEFAULT_OUTPUT_TOKENS,
        model=LARGE_MODEL,
        infrastructure=infrastructure,
    )

    cost_per_request = calculate_request_cost(
        request
    )

    monthly_cost = calculate_monthly_cost(
        cost_per_request,
        monthly_requests=100_000,
    )

    return {
        "model": LARGE_MODEL.name,
        "input_tokens": DEFAULT_INPUT_TOKENS,
        "output_tokens": DEFAULT_OUTPUT_TOKENS,
        "infrastructure_cost_per_request":
            infrastructure.total_per_request,
        "cost_per_request": round(
            cost_per_request,
            6,
        ),
        "monthly_requests": 100_000,
        "monthly_cost": round(
            monthly_cost,
            2,
        ),
    }


@app.get("/cost/optimization")
async def optimization():

    return {
        "scenarios": run_optimization()
    }