from app.tools.pipeline_tools import table_schema_tool


def investigate_data(table_name: str) -> dict:
    result = table_schema_tool(table_name)

    if not result.get("success"):
        return {
            "agent": "data_agent",
            "status": "FAILED",
            "findings": [],
            "confidence": 0.0,
            "error": result.get("error"),
        }

    return {
        "agent": "data_agent",
        "status": "COMPLETED",
        "findings": [
            f"Table {table_name} contains columns: "
            f"{', '.join(result.get('columns', []))}"
        ],
        "raw_evidence": result,
        "confidence": 0.90,
    }