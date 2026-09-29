from src.state import ReimbursementState

from langgraph.graph import StateGraph, START, END


def validate_reimbursement(state: ReimbursementState):
    print("→ Validating reimbursement")

    if state["amount"] <= 0:
        return {
            "validation_status": "invalid",
            "validation_message": (
                "Reimbursement amount must be greater than zero."
            ),
        }

    if not state["expense_type"]:
        return {
            "validation_status": "invalid",
            "validation_message": (
                "Expense type is required."
            ),
        }

    if not state["description"]:
        return {
            "validation_status": "invalid",
            "validation_message": (
                "Expense description is required."
            ),
        }

    return {
        "validation_status": "valid",
        "validation_message": (
            "Reimbursement claim is valid."
        ),
    }


def determine_approval(state: ReimbursementState):
    print("→ Determining approval requirement")

    if state["amount"] > 5000:
        return {
            "approval_required": True,
            "approval_status": "pending",
        }

    return {
        "approval_required": False,
        "approval_status": "not_required",
    }


builder = StateGraph(ReimbursementState)

builder.add_node(
    "validate_reimbursement",
    validate_reimbursement,
)

builder.add_node(
    "determine_approval",
    determine_approval,
)

builder.add_edge(
    START,
    "validate_reimbursement",
)

builder.add_edge(
    "validate_reimbursement",
    "determine_approval",
)

builder.add_edge(
    "determine_approval",
    END,
)

graph = builder.compile()


if __name__ == "__main__":

    initial_state: ReimbursementState = {
        "employee_id": "EMP-1042",
        "expense_type": "Travel",
        "amount": 8500.00,
        "description": (
            "Flight and accommodation for client meeting"
        ),

        "validation_status": "",
        "validation_message": "",

        "approval_required": False,
        "approval_status": "",

        "processing_status": "",
        "final_response": "",
    }

    print("\n========== STREAMING EXECUTION ==========\n")

    for event in graph.stream(initial_state):
        print("\nEVENT:")
        print(event)

    print("\n========== STREAM COMPLETE ==========")