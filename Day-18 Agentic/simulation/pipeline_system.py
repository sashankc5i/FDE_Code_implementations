from typing import Any


PIPELINE_DATA = {
    "customer_360": {
        "pipeline_id": "customer_360",
        "name": "Customer 360 Pipeline",
        "status": "FAILED",
        "last_run": "2026-09-16T02:14:32",
        "failure_stage": "silver_transformation",
        "error": "AnalysisException: Cannot resolve column 'customer_segment'",
    }
}


def get_pipeline_status(pipeline_id: str) -> dict[str, Any]:
    """
    Simulates querying an enterprise pipeline monitoring system.
    """

    pipeline = PIPELINE_DATA.get(pipeline_id)

    if pipeline is None:
        return {
            "success": False,
            "error": f"Pipeline '{pipeline_id}' not found.",
        }

    return {
        "success": True,
        "pipeline": pipeline,
    }