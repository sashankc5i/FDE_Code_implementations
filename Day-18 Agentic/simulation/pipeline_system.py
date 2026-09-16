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
def find_pipeline(name: str) -> dict[str, Any]:
    """
    Simulates searching for a pipeline by human-readable name.
    """

    normalized_name = name.strip().lower()

    exact_matches = []
    partial_matches = []

    for pipeline_id, pipeline in PIPELINE_DATA.items():

        pipeline_name = pipeline["name"].strip().lower()

        # Exact match
        if pipeline_name == normalized_name:
            exact_matches.append(pipeline)

        # Partial match
        elif (
            normalized_name in pipeline_name
            or pipeline_name in normalized_name
        ):
            partial_matches.append(pipeline)

    matches = exact_matches or partial_matches

    if len(matches) == 1:
        pipeline = matches[0]

        return {
            "success": True,
            "pipeline_id": pipeline["pipeline_id"],
            "name": pipeline["name"],
        }

    if len(matches) > 1:
        return {
            "success": False,
            "error": "Multiple pipelines matched the provided name.",
            "matches": [
                {
                    "pipeline_id": p["pipeline_id"],
                    "name": p["name"],
                }
                for p in matches
            ],
        }

    return {
        "success": False,
        "error": f"No pipeline found matching '{name}'.",
    }
PIPELINE_LOGS = {
    "customer_360": [
        {
            "timestamp": "2026-09-16T02:14:21",
            "level": "INFO",
            "message": "Silver transformation started",
        },
        {
            "timestamp": "2026-09-16T02:14:28",
            "level": "INFO",
            "message": "Reading source table customer_master",
        },
        {
            "timestamp": "2026-09-16T02:14:31",
            "level": "ERROR",
            "message": (
                "AnalysisException: Cannot resolve column "
                "'customer_segment'"
            ),
        },
    ]
}


def get_pipeline_logs(pipeline_id: str) -> dict[str, Any]:
    """
    Simulates retrieving pipeline execution logs.
    """

    logs = PIPELINE_LOGS.get(pipeline_id)

    if logs is None:
        return {
            "success": False,
            "error": f"No logs found for pipeline '{pipeline_id}'.",
        }

    return {
        "success": True,
        "pipeline_id": pipeline_id,
        "logs": logs,
    }
TABLE_SCHEMAS = {
    "customer_master": {
        "columns": [
            "customer_id",
            "customer_name",
            "email",
            "country",
            "segment",
            "created_date",
        ]
    }
}


def get_table_schema(table_name: str) -> dict[str, Any]:
    """
    Simulates retrieving the current schema of an enterprise table.
    """

    schema = TABLE_SCHEMAS.get(table_name)

    if schema is None:
        return {
            "success": False,
            "error": f"Table '{table_name}' not found.",
        }

    return {
        "success": True,
        "table_name": table_name,
        "columns": schema["columns"],
    }