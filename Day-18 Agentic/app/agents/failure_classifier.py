from app.models.incident_state import IncidentState

from app.workflows.failure_types import (
    SCHEMA_DRIFT,
    DATA_QUALITY,
    INFRASTRUCTURE,
    DEPLOYMENT,
    UNKNOWN,
)


def classify_failure(
    state: IncidentState,
) -> str:

    has_schema_error = False
    has_schema_evidence = False

    has_data_quality_error = False
    has_infrastructure_error = False
    has_deployment_error = False

    for observation in state.observations:

        source = observation["source"]
        data = observation["data"]

        text = str(data).lower()

        # Schema error evidence
        if (
            "analysisexception" in text
            and "cannot resolve column" in text
        ):
            has_schema_error = True

        # Actual schema evidence
        if source == "get_table_schema":
            if data.get("success"):
                has_schema_evidence = True

        # Data quality
        if (
            "data quality" in text
            or "null percentage" in text
        ):
            has_data_quality_error = True

        # Infrastructure
        if (
            "executor" in text
            or "out of memory" in text
            or "cluster" in text
        ):
            has_infrastructure_error = True

        # Deployment
        if (
            "deployment" in text
            or "deployed version" in text
        ):
            has_deployment_error = True

    if has_schema_error and has_schema_evidence:
        return SCHEMA_DRIFT

    if has_data_quality_error:
        return DATA_QUALITY

    if has_infrastructure_error:
        return INFRASTRUCTURE

    if has_deployment_error:
        return DEPLOYMENT

    if has_schema_error:
        return SCHEMA_DRIFT

    return UNKNOWN