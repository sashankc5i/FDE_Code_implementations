import asyncio
import time
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


app = FastAPI(title="AI Performance Optimization Lab")


# ============================================================
# Simulated downstream systems
# ============================================================

async def get_customer_data():
    await asyncio.sleep(0.5)

    return {
        "customer_segment": "Enterprise",
        "customer_count": 1240,
        "churn_rate": 0.087,
        "lifetime_value": 18250,
    }


async def get_pricing_data():
    await asyncio.sleep(0.4)

    return {
        "average_price_index": 99.7,
        "discount_rate": 0.12,
        "price_change": -0.8,
    }


async def get_market_data():
    await asyncio.sleep(0.7)

    return {
        "market_demand_index": 88.2,
        "industry_growth": -4.7,
        "competitor_activity": "HIGH",
    }


# ============================================================
# Simulated LLM
# ============================================================

MODEL_CONFIG = {
    "small": {
        "latency": 0.6,
        "cost_per_1k_input": 1.0,
        "cost_per_1k_output": 2.0,
    },
    "large": {
        "latency": 1.2,
        "cost_per_1k_input": 4.0,
        "cost_per_1k_output": 8.0,
    },
}


async def simulated_llm(
    prompt: str,
    model: str = "large",
):
    config = MODEL_CONFIG[model]

    input_tokens = len(prompt.split())
    output_tokens = 500

    start = time.perf_counter()

    await asyncio.sleep(config["latency"])

    elapsed = time.perf_counter() - start

    cost_units = (
        (input_tokens / 1000) * config["cost_per_1k_input"]
        + (output_tokens / 1000) * config["cost_per_1k_output"]
    )

    response = (
        f"Business analysis generated using {model} model. "
        f"Input tokens: {input_tokens}. "
        f"Output tokens: {output_tokens}."
    )

    return {
        "response": response,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_units": round(cost_units, 4),
        "model": model,
        "generation_latency": round(elapsed, 4),
    }


# ============================================================
# Prompt construction
# ============================================================

def build_large_prompt(
    customer: Dict,
    pricing: Dict,
    market: Dict,
):
    repeated_context = """
    You are an enterprise business analytics assistant.

    Analyze customer behavior, pricing changes, market conditions,
    revenue trends, customer health, historical business performance,
    regional performance, product performance, competitor activity,
    customer segmentation, sales pipeline, marketing performance,
    demand patterns, pricing elasticity, customer lifetime value,
    churn behavior, acquisition behavior, retention behavior,
    and overall commercial performance.

    Provide detailed reasoning and identify important business drivers.
    """

    return f"""
    {repeated_context}

    Customer Data:
    {customer}

    Pricing Data:
    {pricing}

    Market Data:
    {market}

    Provide a detailed business analysis.
    """


def build_compressed_prompt(
    customer: Dict,
    pricing: Dict,
    market: Dict,
):
    return f"""
    Analyze business performance using the following evidence.

    Customer:
    segment={customer["customer_segment"]}
    customers={customer["customer_count"]}
    churn={customer["churn_rate"]}
    ltv={customer["lifetime_value"]}

    Pricing:
    price_index={pricing["average_price_index"]}
    discount={pricing["discount_rate"]}
    price_change={pricing["price_change"]}

    Market:
    demand={market["market_demand_index"]}
    growth={market["industry_growth"]}
    competitor_activity={market["competitor_activity"]}

    Identify the major business drivers.
    """


# ============================================================
# Cache
# ============================================================

CACHE = {}


# ============================================================
# Baseline
# ============================================================

async def baseline_pipeline():

    start = time.perf_counter()

    # Sequential execution
    customer = await get_customer_data()
    pricing = await get_pricing_data()
    market = await get_market_data()

    prompt = build_large_prompt(
        customer,
        pricing,
        market,
    )

    llm_result = await simulated_llm(
        prompt,
        model="large",
    )

    total_latency = time.perf_counter() - start

    return {
        "strategy": "baseline",
        "ttft": round(total_latency, 4),
        "total_latency": round(total_latency, 4),
        "input_tokens": llm_result["input_tokens"],
        "output_tokens": llm_result["output_tokens"],
        "cost_units": llm_result["cost_units"],
        "cache_hit": False,
        "model": llm_result["model"],
    }


# ============================================================
# Async optimization
# ============================================================

async def async_pipeline():

    start = time.perf_counter()

    customer, pricing, market = await asyncio.gather(
        get_customer_data(),
        get_pricing_data(),
        get_market_data(),
    )

    prompt = build_large_prompt(
        customer,
        pricing,
        market,
    )

    llm_result = await simulated_llm(
        prompt,
        model="large",
    )

    total_latency = time.perf_counter() - start

    return {
        "strategy": "async",
        "ttft": round(total_latency, 4),
        "total_latency": round(total_latency, 4),
        "input_tokens": llm_result["input_tokens"],
        "output_tokens": llm_result["output_tokens"],
        "cost_units": llm_result["cost_units"],
        "cache_hit": False,
        "model": llm_result["model"],
    }


# ============================================================
# Prompt compression optimization
# ============================================================

async def compressed_pipeline():

    start = time.perf_counter()

    customer, pricing, market = await asyncio.gather(
        get_customer_data(),
        get_pricing_data(),
        get_market_data(),
    )

    prompt = build_compressed_prompt(
        customer,
        pricing,
        market,
    )

    llm_result = await simulated_llm(
        prompt,
        model="large",
    )

    total_latency = time.perf_counter() - start

    return {
        "strategy": "compressed",
        "ttft": round(total_latency, 4),
        "total_latency": round(total_latency, 4),
        "input_tokens": llm_result["input_tokens"],
        "output_tokens": llm_result["output_tokens"],
        "cost_units": llm_result["cost_units"],
        "cache_hit": False,
        "model": llm_result["model"],
    }


# ============================================================
# Cache optimization
# ============================================================

async def cached_pipeline():

    cache_key = "enterprise-business-analysis"

    if cache_key in CACHE:
        result = CACHE[cache_key].copy()
        result["strategy"] = "cached"
        result["cache_hit"] = True
        result["ttft"] = 0.001
        result["total_latency"] = 0.001
        result["cost_units"] = 0.0

        return result

    result = await compressed_pipeline()

    result["strategy"] = "cached"
    result["cache_hit"] = False

    CACHE[cache_key] = result.copy()

    return result


# ============================================================
# Model routing
# ============================================================

async def routed_pipeline(complexity: str = "simple"):

    start = time.perf_counter()

    customer, pricing, market = await asyncio.gather(
        get_customer_data(),
        get_pricing_data(),
        get_market_data(),
    )

    prompt = build_compressed_prompt(
        customer,
        pricing,
        market,
    )

    if complexity == "simple":
        model = "small"
    else:
        model = "large"

    llm_result = await simulated_llm(
        prompt,
        model=model,
    )

    total_latency = time.perf_counter() - start

    return {
        "strategy": "routing",
        "ttft": round(total_latency, 4),
        "total_latency": round(total_latency, 4),
        "input_tokens": llm_result["input_tokens"],
        "output_tokens": llm_result["output_tokens"],
        "cost_units": llm_result["cost_units"],
        "cache_hit": False,
        "model": llm_result["model"],
    }


# ============================================================
# Streaming
# ============================================================

async def streaming_generator():

    customer, pricing, market = await asyncio.gather(
        get_customer_data(),
        get_pricing_data(),
        get_market_data(),
    )

    prompt = build_compressed_prompt(
        customer,
        pricing,
        market,
    )

    # Simulate model preparation / TTFT
    await asyncio.sleep(0.6)

    response = (
        "Business analysis generated using streaming execution. "
        "Customer health is stable. "
        "Pricing impact is limited. "
        "Market demand shows some deterioration."
    )

    words = response.split()

    for word in words:
        await asyncio.sleep(0.05)
        yield word + " "


# ============================================================
# API
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


@app.get("/chat")
async def chat(
    strategy: str = "baseline",
    complexity: str = "simple",
):

    if strategy == "baseline":
        return await baseline_pipeline()

    if strategy == "async":
        return await async_pipeline()

    if strategy == "compressed":
        return await compressed_pipeline()

    if strategy == "cached":
        return await cached_pipeline()

    if strategy == "routing":
        return await routed_pipeline(complexity)

    if strategy == "streaming":
        return StreamingResponse(
            streaming_generator(),
            media_type="text/plain",
        )

    return {
        "error": "Unknown strategy"
    }