from app.models.evaluation import IncidentEvaluation
from app.models.incident_state import IncidentState

from simulation.incident_ground_truth import GROUND_TRUTH


def evaluate_incident(
    state: IncidentState,
) -> IncidentEvaluation:
    """
    Evaluate the outcome and execution quality of an incident
    investigation.

    Evaluation is based on:
    - Tool execution results
    - Specialist agent results
    - Incident classification
    - Ground-truth diagnosis
    - Human escalation
    """

    successful_tools = 0
    failed_tools = 0

    specialist_agents = set()
    specialist_failures = 0

    # ---------------------------------------------------------
    # Inspect observations
    # ---------------------------------------------------------

    for observation in state.observations:

        source = observation.get("source")
        data = observation.get("data", {})

        # -----------------------------------------------------
        # Tool success / failure
        # -----------------------------------------------------

        if data.get("success") is True:
            successful_tools += 1

        elif data.get("success") is False:
            failed_tools += 1

        # -----------------------------------------------------
        # Specialist agent tracking
        # -----------------------------------------------------

        if source and source.endswith("_agent"):

            specialist_agents.add(source)

            if data.get("status") == "FAILED":
                specialist_failures += 1

    # ---------------------------------------------------------
    # Ground truth comparison
    # ---------------------------------------------------------

    ground_truth = GROUND_TRUTH.get(
        state.incident_id
    )

    diagnosis_correct = False

    if ground_truth is not None:

        expected_failure_type = (
            ground_truth.get("failure_type")
        )

        diagnosis_correct = (
            state.failure_type
            == expected_failure_type
        )

    # ---------------------------------------------------------
    # Investigation success
    # ---------------------------------------------------------

    investigation_success = (
        diagnosis_correct
        and state.current_state
        in {
            "CLASSIFYING",
            "REMEDIATING",
            "VALIDATING",
            "SUCCESS",
        }
    )

    # ---------------------------------------------------------
    # Build evaluation object
    # ---------------------------------------------------------

    return IncidentEvaluation(
        incident_id=state.incident_id,

        failure_type=state.failure_type,

        llm_iterations=state.llm_iterations,

        tool_calls=state.tool_calls,

        successful_tool_calls=successful_tools,

        failed_tool_calls=failed_tools,

        specialist_agents=list(
            specialist_agents
        ),

        specialist_failures=specialist_failures,

        human_escalation=state.requires_human,

        remediation_attempted=False,

        remediation_success=False,

        validation_attempted=False,

        validation_success=False,

        investigation_success=investigation_success,

        diagnosis_correct=diagnosis_correct,
    )