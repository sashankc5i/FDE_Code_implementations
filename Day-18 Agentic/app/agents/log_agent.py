from app.tools.pipeline_tools import pipeline_logs_tool


def investigate_logs(pipeline_id: str) -> dict:
    result = pipeline_logs_tool(pipeline_id)

    if not result.get("success"):
        return {
            "agent": "log_agent",
            "status": "FAILED",
            "findings": [],
            "confidence": 0.0,
            "error": result.get("error"),
        }

    findings = []

    for log in result.get("logs", []):
        if log.get("level") == "ERROR":
            findings.append(log["message"])

    return {
        "agent": "log_agent",
        "status": "COMPLETED",
        "findings": findings,
        "raw_evidence": result,
        "confidence": 0.95 if findings else 0.5,
    }