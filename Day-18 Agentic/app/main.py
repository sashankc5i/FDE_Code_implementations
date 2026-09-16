from app.agents.incident_agent import run_agent
from app.models.incident_state import IncidentState
from app.workflows.checkpoint_store import load_state


INCIDENT_ID = "INC-2026-0916-001"


state = load_state(INCIDENT_ID)

if state is None:
    state = IncidentState(
        incident_id=INCIDENT_ID
    )

else:
    print(
        f"Resuming incident {INCIDENT_ID}"
    )

    print(
        f"Previous state: {state.current_state}"
    )

    print(
        f"Previous tool calls: {state.tool_calls}"
    )


result = run_agent(
    "Why did the Customer 360 pipeline fail?",
    state,
)

print("\n=== INCIDENT AGENT ===")
print(result)

print("\n=== INCIDENT STATE ===")
print(state.model_dump_json(indent=2))