import json
from pathlib import Path

from app.models.incident_state import IncidentState


CHECKPOINT_DIR = Path("checkpoints")

CHECKPOINT_DIR.mkdir(exist_ok=True)


def _checkpoint_path(incident_id: str) -> Path:
    return CHECKPOINT_DIR / f"{incident_id}.json"


def save_state(state: IncidentState) -> None:
    path = _checkpoint_path(state.incident_id)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            state.model_dump(),
            file,
            indent=2,
        )


def load_state(incident_id: str) -> IncidentState | None:
    path = _checkpoint_path(incident_id)

    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return IncidentState(**data)