from typing import Any, Optional

from pydantic import BaseModel, Field


class IncidentState(BaseModel):
    incident_id: str

    pipeline_id: Optional[str] = None

    current_state: str = "START"

    failure_type: Optional[str] = None

    observations: list[dict[str, Any]] = Field(default_factory=list)

    actions_taken: list[str] = Field(default_factory=list)

    llm_iterations: int = 0

    tool_calls: int = 0

    confidence: float = 0.0

    requires_human: bool = False

    last_error: Optional[str] = None