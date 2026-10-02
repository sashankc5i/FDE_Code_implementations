from cost_model import ModelPricing


SMALL_MODEL = ModelPricing(
    name="small-model",
    input_cost_per_million=1.0,
    output_cost_per_million=4.0,
)


LARGE_MODEL = ModelPricing(
    name="large-model",
    input_cost_per_million=5.0,
    output_cost_per_million=20.0,
)


DEFAULT_INPUT_TOKENS = 2_000
DEFAULT_OUTPUT_TOKENS = 500


def create_request(model):

    return {
        "input_tokens": DEFAULT_INPUT_TOKENS,
        "output_tokens": DEFAULT_OUTPUT_TOKENS,
        "model": model,
    }