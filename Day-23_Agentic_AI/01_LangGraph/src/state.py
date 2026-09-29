from typing import TypedDict


class ReimbursementState(TypedDict):
    """
    Shared state for the reimbursement approval workflow.

    Each LangGraph node can read the current state and
    return updates to it.
    """

    employee_id: str
    expense_type: str
    amount: float
    description: str

    validation_status: str
    validation_message: str

    approval_required: bool
    approval_status: str

    processing_status: str
    final_response: str