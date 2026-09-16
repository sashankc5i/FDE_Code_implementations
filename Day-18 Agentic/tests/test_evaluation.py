from app.evaluation.evaluator import evaluate_incident
from app.models.incident_state import IncidentState


def test_incident_evaluation():

    state = IncidentState(
        incident_id="INC-001",
        pipeline_id="customer_360",
        current_state="CLASSIFYING",
        failure_type="SCHEMA_DRIFT",
        llm_iterations=5,
        tool_calls=4,
        observations=[
            {
                "source": "get_pipeline_status",
                "data": {
                    "success": True
                },
            },
            {
                "source": "get_pipeline_logs",
                "data": {
                    "success": True
                },
            },
            {
                "source": "get_table_schema",
                "data": {
                    "success": True
                },
            },
        ],
    )

    evaluation = evaluate_incident(state)

    assert evaluation.incident_id == "INC-001"

    assert evaluation.failure_type == "SCHEMA_DRIFT"

    assert evaluation.tool_calls == 4

    assert evaluation.successful_tool_calls == 3

    assert evaluation.failed_tool_calls == 0

    assert evaluation.investigation_success is True