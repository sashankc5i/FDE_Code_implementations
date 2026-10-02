from cost_model import (
    InfrastructureCost,
    RequestCost,
    calculate_request_cost,
)
from simulator import SMALL_MODEL, LARGE_MODEL


MONTHLY_REQUESTS = 100_000


def calculate_scenario(
    name,
    model,
    input_tokens,
    output_tokens,
    cache_hit_rate=0.0,
):

    infrastructure = InfrastructureCost()

    uncached_request = RequestCost(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        model=model,
        infrastructure=infrastructure,
    )

    cost_per_uncached_request = calculate_request_cost(
        uncached_request
    )

    effective_cost_per_request = (
        cost_per_uncached_request
        * (1 - cache_hit_rate)
    )

    monthly_cost = (
        effective_cost_per_request
        * MONTHLY_REQUESTS
    )

    return {
        "scenario": name,
        "model": model.name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cache_hit_rate": cache_hit_rate,
        "cost_per_request": round(
            effective_cost_per_request,
            6,
        ),
        "monthly_cost": round(
            monthly_cost,
            2,
        ),
    }


def calculate_savings(
    baseline_cost,
    optimized_cost,
):

    savings = baseline_cost - optimized_cost

    savings_percent = (
        savings / baseline_cost
    ) * 100

    return {
        "monthly_savings": round(
            savings,
            2,
        ),
        "savings_percent": round(
            savings_percent,
            2,
        ),
    }


def run_optimization():

    baseline = calculate_scenario(
        name="baseline",
        model=LARGE_MODEL,
        input_tokens=2_000,
        output_tokens=500,
    )

    caching = calculate_scenario(
        name="caching",
        model=LARGE_MODEL,
        input_tokens=2_000,
        output_tokens=500,
        cache_hit_rate=0.30,
    )

    model_routing = calculate_scenario(
        name="model_routing",
        model=SMALL_MODEL,
        input_tokens=2_000,
        output_tokens=500,
    )

    prompt_optimization = calculate_scenario(
        name="prompt_optimization",
        model=LARGE_MODEL,
        input_tokens=1_000,
        output_tokens=500,
    )

    combined = calculate_scenario(
        name="combined",
        model=SMALL_MODEL,
        input_tokens=1_000,
        output_tokens=500,
        cache_hit_rate=0.30,
    )

    scenarios = [
        baseline,
        caching,
        model_routing,
        prompt_optimization,
        combined,
    ]

    baseline_monthly = baseline["monthly_cost"]

    for scenario in scenarios:

        savings = calculate_savings(
            baseline_monthly,
            scenario["monthly_cost"],
        )

        scenario.update(savings)

    return scenarios