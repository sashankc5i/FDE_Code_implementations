from simulation.pipeline_system import (
    find_pipeline,
    get_pipeline_status,
    get_pipeline_logs,
    get_table_schema,
)
from simulation.remediation_system import (
    restart_pipeline,
    validate_pipeline,
)

def restart_pipeline_tool(
    pipeline_id: str,
) -> dict:
    return restart_pipeline(pipeline_id)


def validate_pipeline_tool(
    pipeline_id: str,
) -> dict:
    return validate_pipeline(pipeline_id)

def pipeline_status_tool(pipeline_id: str) -> dict:
    """
    Tool exposed to the agent for checking pipeline status.
    """

    return get_pipeline_status(pipeline_id)
from simulation.pipeline_system import (
    find_pipeline,
    get_pipeline_status,
)


def pipeline_search_tool(name: str) -> dict:
    """
    Tool exposed to the agent for finding a pipeline
    using a human-readable name.
    """

    return find_pipeline(name)


def pipeline_status_tool(pipeline_id: str) -> dict:
    """
    Tool exposed to the agent for checking pipeline status.
    """

    return get_pipeline_status(pipeline_id)

def pipeline_logs_tool(pipeline_id: str) -> dict:
    """
    Tool exposed to the agent for retrieving pipeline logs.
    """

    return get_pipeline_logs(pipeline_id)

def table_schema_tool(table_name: str) -> dict:
    """
    Tool exposed to the agent for retrieving table schema.
    """

    return get_table_schema(table_name)