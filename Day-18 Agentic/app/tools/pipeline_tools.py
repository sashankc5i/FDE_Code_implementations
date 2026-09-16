from simulation.pipeline_system import get_pipeline_status


def pipeline_status_tool(pipeline_id: str) -> dict:
    """
    Tool exposed to the agent for checking pipeline status.
    """

    return get_pipeline_status(pipeline_id)