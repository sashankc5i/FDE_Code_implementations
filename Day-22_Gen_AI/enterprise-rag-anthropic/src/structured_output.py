from pydantic import BaseModel, Field


class EmployeeAssessment(BaseModel):
    employee_id: str
    status: str
    confidence: float = Field(
        ge=0,
        le=1
    )
    reason: str


if __name__ == "__main__":
    result = EmployeeAssessment(
        employee_id="202534571",
        status="bench",
        confidence=0.91,
        reason="No active project assignment"
    )

    print("\n========== STRUCTURED OUTPUT ==========")
    print(result)

    print("\n========== AS DICTIONARY ==========")
    print(result.model_dump())