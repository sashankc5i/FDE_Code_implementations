from app.tools.pipeline_tools import validate_pipeline_tool


def validate_recovery(
    pipeline_id: str,
) -> dict:

    result = validate_pipeline_tool(
        pipeline_id
    )

    if not result.get("success"):

        return {
            "agent": "validation_agent",
            "status": "FAILED",
            "valid": False,
            "error": result.get("error"),
        }

    is_success = (
        result.get("status") == "SUCCESS"
    )

    return {
        "agent": "validation_agent",
        "status": "COMPLETED",
        "valid": is_success,
        "result": result,
    }