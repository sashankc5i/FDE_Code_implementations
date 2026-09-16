from app.models.incident_state import IncidentState
from app.workflows.states import (
    START,
    INVESTIGATING,
    CLASSIFYING,
    REMEDIATING,
    APPROVAL_PENDING,
    VALIDATING,
    SUCCESS,
    FAILED,
    ESCALATED,
)


VALID_TRANSITIONS = {
    START: {
        INVESTIGATING,
    },

    INVESTIGATING: {
        CLASSIFYING,
        FAILED,
        ESCALATED,
    },

    CLASSIFYING: {
        REMEDIATING,
        APPROVAL_PENDING,
        ESCALATED,
        FAILED,
    },

    REMEDIATING: {
        VALIDATING,
        APPROVAL_PENDING,
        FAILED,
        ESCALATED,
    },

    APPROVAL_PENDING: {
        REMEDIATING,
        ESCALATED,
        FAILED,
    },

    VALIDATING: {
        SUCCESS,
        FAILED,
        ESCALATED,
    },

    SUCCESS: set(),
    FAILED: set(),
    ESCALATED: set(),
}


def transition(
    state: IncidentState,
    new_state: str,
) -> None:

    current_state = state.current_state

    allowed_states = VALID_TRANSITIONS.get(
        current_state,
        set(),
    )

    if new_state not in allowed_states:
        raise ValueError(
            f"Invalid state transition: "
            f"{current_state} -> {new_state}"
        )

    state.current_state = new_state