from dataclasses import dataclass


@dataclass
class ModelPricing:
    name: str
    input_cost_per_million: float
    output_cost_per_million: float


@dataclass
class InfrastructureCost:
    compute_per_request: float = 0.001
    database_per_request: float = 0.0005
    vector_db_per_request: float = 0.0005
    monitoring_per_request: float = 0.0002

    @property
    def total_per_request(self):
        return (
            self.compute_per_request
            + self.database_per_request
            + self.vector_db_per_request
            + self.monitoring_per_request
        )


@dataclass
class RequestCost:
    input_tokens: int
    output_tokens: int
    model: ModelPricing
    infrastructure: InfrastructureCost
    cache_hit: bool = False


def calculate_token_cost(
    input_tokens: int,
    output_tokens: int,
    model: ModelPricing,
):
    input_cost = (
        input_tokens / 1_000_000
    ) * model.input_cost_per_million

    output_cost = (
        output_tokens / 1_000_000
    ) * model.output_cost_per_million

    return input_cost + output_cost


def calculate_request_cost(request: RequestCost):

    if request.cache_hit:
        return 0.0

    token_cost = calculate_token_cost(
        request.input_tokens,
        request.output_tokens,
        request.model,
    )

    infrastructure_cost = (
        request.infrastructure.total_per_request
    )

    return token_cost + infrastructure_cost


def calculate_monthly_cost(
    cost_per_request: float,
    monthly_requests: int,
):
    return cost_per_request * monthly_requests