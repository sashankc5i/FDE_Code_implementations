from app.tools.pipeline_tools import restart_pipeline_tool


def remediate_pipeline(
    pipeline_id: str,
    approved: bool = False,
) -> dict:

    if not approved:

        return {
            "agent": "remediation_agent",
            "status": "BLOCKED",
            "requires_human": True,
            "action": "restart_pipeline",
            "reason": (
                "Pipeline restart requires human approval."
            ),
        }

    result = restart_pipeline_tool(
        pipeline_id
    )

    if not result.get("success"):

        return {
            "agent": "remediation_agent",
            "status": "FAILED",
            "requires_human": False,
            "action": "restart_pipeline",
            "error": result.get("error"),
        }

    return {
        "agent": "remediation_agent",
        "status": "COMPLETED",
        "requires_human": False,
        "action": "restart_pipeline",
        "result": result,
    }
def determine_remediation(
    failure_type: str,
) -> dict:

    if failure_type == "SCHEMA_DRIFT":

        return {
            "remediation_available": False,
            "requires_human": True,
            "reason": (
                "Schema mismatch requires transformation "
                "logic or schema correction before rerun."
            ),
        }

    if failure_type == "DATA_QUALITY":

        return {
            "remediation_available": False,
            "requires_human": True,
            "reason": (
                "Data quality failures require investigation "
                "before automated remediation."
            ),
        }

    if failure_type == "INFRASTRUCTURE":

        return {
            "remediation_available": True,
            "requires_human": True,
            "action": "restart_pipeline",
            "reason": (
                "Infrastructure recovery may be attempted "
                "after approval."
            ),
        }

    return {
        "remediation_available": False,
        "requires_human": True,
        "reason": (
            "No safe automated remediation is available."
        ),
    }