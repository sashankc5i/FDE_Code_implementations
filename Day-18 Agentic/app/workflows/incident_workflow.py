from app.agents.failure_classifier import classify_failure
from app.agents.remediation_agent import determine_remediation
from app.agents.validation_agent import validate_recovery
from app.models.incident_state import IncidentState
from app.workflows.state_manager import (
    update_state,
    record_error,
)


def classify_incident(
    state: IncidentState,
) -> None:

    failure_type = classify_failure(state)

    state.failure_type = failure_type

    update_state(
        state,
        "CLASSIFYING",
    )


def determine_next_action(
    state: IncidentState,
) -> dict:

    remediation = determine_remediation(
        state.failure_type
    )

    if not remediation.get(
        "remediation_available",
        False,
    ):
        state.requires_human = True
        state.approval_required = False

        return remediation

    if remediation.get("requires_human"):
        state.requires_human = True
        state.approval_required = True
        state.approval_status = "PENDING"
        state.pending_action = remediation.get(
            "action"
        )

        update_state(
            state,
            "APPROVAL_PENDING",
        )

        return remediation

    return remediation


def approve_action(
    state: IncidentState,
) -> None:

    if state.current_state != "APPROVAL_PENDING":
        raise ValueError(
            "Incident is not waiting for approval."
        )

    state.approval_status = "APPROVED"

    update_state(
        state,
        "REMEDIATING",
    )


def reject_action(
    state: IncidentState,
) -> None:

    if state.current_state != "APPROVAL_PENDING":
        raise ValueError(
            "Incident is not waiting for approval."
        )

    state.approval_status = "REJECTED"
    state.requires_human = True

    update_state(
        state,
        "ESCALATED",
    )


def validate_incident(
    state: IncidentState,
) -> dict:

    if not state.pipeline_id:
        error = "Pipeline ID is missing."

        record_error(
            state,
            error,
        )

        update_state(
            state,
            "FAILED",
        )

        return {
            "success": False,
            "error": error,
        }

    result = validate_recovery(
        state.pipeline_id
    )

    if result.get("valid"):
        update_state(
            state,
            "SUCCESS",
        )

        return {
            "success": True,
            "result": result,
        }

    update_state(
        state,
        "FAILED",
    )

    return {
        "success": False,
        "result": result,
    }