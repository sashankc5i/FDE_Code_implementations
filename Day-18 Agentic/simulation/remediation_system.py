from typing import Any

from simulation.pipeline_system import PIPELINE_DATA


def restart_pipeline(
    pipeline_id: str,
) -> dict[str, Any]:

    pipeline = PIPELINE_DATA.get(pipeline_id)

    if pipeline is None:
        return {
            "success": False,
            "error": f"Pipeline '{pipeline_id}' not found.",
        }

    # Simulate successful remediation.
    pipeline["status"] = "RUNNING"

    return {
        "success": True,
        "pipeline_id": pipeline_id,
        "status": "RUNNING",
        "message": "Pipeline restart initiated.",
    }


def validate_pipeline(
    pipeline_id: str,
) -> dict[str, Any]:

    pipeline = PIPELINE_DATA.get(pipeline_id)

    if pipeline is None:
        return {
            "success": False,
            "error": f"Pipeline '{pipeline_id}' not found.",
        }

    # Simulate successful pipeline recovery.
    pipeline["status"] = "SUCCESS"

    return {
        "success": True,
        "pipeline_id": pipeline_id,
        "status": "SUCCESS",
        "message": "Pipeline completed successfully.",
    }