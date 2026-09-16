from app.models.incident_state import IncidentState
from app.workflows.checkpoint_store import save_state
from app.workflows.state_machine import transition


def add_observation(
    state: IncidentState,
    source: str,
    data: dict,
) -> None:

    state.observations.append(
        {
            "source": source,
            "data": data,
        }
    )

    if (
        source == "find_pipeline"
        and data.get("success")
        and data.get("pipeline_id")
    ):
        state.pipeline_id = data["pipeline_id"]

    save_state(state)


def record_action(
    state: IncidentState,
    action: str,
) -> None:

    state.actions_taken.append(action)

    save_state(state)


def update_state(
    state: IncidentState,
    new_state: str,
) -> None:

    transition(
        state,
        new_state,
    )

    save_state(state)


def record_error(
    state: IncidentState,
    error: str,
) -> None:

    state.last_error = error

    save_state(state)