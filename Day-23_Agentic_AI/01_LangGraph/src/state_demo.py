from src.state import ReimbursementState
from langgraph.graph import StateGraph, START, END


def validate_reimbursement(state: ReimbursementState):
    """
    Validate the reimbursement claim.
    """

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


def route_validation(state: ReimbursementState):
    """
    Decide what should happen after validation.
    """

    if state["validation_status"] == "valid":
        return "valid"

    return "invalid"


def determine_approval(state: ReimbursementState):
    """
    Determine whether human approval is required.

    Claims above ₹5,000 require approval.
    """

    if state["amount"] > 5000:
        return {
            "approval_required": True,
            "approval_status": "pending",
        }

    return {
        "approval_required": False,
        "approval_status": "not_required",
    }


def route_approval(state: ReimbursementState):
    """
    Decide whether the claim should be automatically
    processed or sent for human approval.
    """

    if state["approval_required"]:
        return "approval_required"

    return "no_approval_required"


def reject_reimbursement(state: ReimbursementState):
    """
    Reject an invalid reimbursement claim.
    """

    return {
        "processing_status": "rejected",
        "final_response": (
            "Your reimbursement claim could not be processed "
            f"because it is invalid: "
            f"{state['validation_message']}"
        ),
    }


def auto_process_reimbursement(state: ReimbursementState):
    """
    Automatically process claims that do not require
    human approval.
    """

    return {
        "processing_status": "processed",
        "final_response": (
            f"Your reimbursement claim for "
            f"₹{state['amount']:.2f} has been automatically processed."
        ),
    }


def request_human_approval(state: ReimbursementState):
    """
    Mark a high-value reimbursement for human approval.

    We will replace this with actual human-in-the-loop
    behavior later.
    """

    return {
        "approval_status": "pending",
        "processing_status": "awaiting_approval",
        "final_response": (
            f"Your reimbursement claim for "
            f"₹{state['amount']:.2f} requires human approval."
        ),
    }


builder = StateGraph(ReimbursementState)


# -------------------------
# Nodes
# -------------------------

builder.add_node(
    "validate_reimbursement",
    validate_reimbursement,
)

builder.add_node(
    "determine_approval",
    determine_approval,
)

builder.add_node(
    "reject_reimbursement",
    reject_reimbursement,
)

builder.add_node(
    "auto_process_reimbursement",
    auto_process_reimbursement,
)

builder.add_node(
    "request_human_approval",
    request_human_approval,
)


# -------------------------
# Fixed edges
# -------------------------

builder.add_edge(
    START,
    "validate_reimbursement",
)


# -------------------------
# Conditional validation route
# -------------------------

builder.add_conditional_edges(
    "validate_reimbursement",
    route_validation,
    {
        "valid": "determine_approval",
        "invalid": "reject_reimbursement",
    },
)


# -------------------------
# Conditional approval route
# -------------------------

builder.add_conditional_edges(
    "determine_approval",
    route_approval,
    {
        "no_approval_required": "auto_process_reimbursement",
        "approval_required": "request_human_approval",
    },
)


# -------------------------
# Terminal edges
# -------------------------

builder.add_edge(
    "reject_reimbursement",
    END,
)

builder.add_edge(
    "auto_process_reimbursement",
    END,
)

builder.add_edge(
    "request_human_approval",
    END,
)


graph = builder.compile()


if __name__ == "__main__":

    initial_state: ReimbursementState = {
        "employee_id": "EMP-1042",
        "expense_type": "Travel",
        "amount": -100.00,
        "description": (
            "Taxi and accommodation expenses for client visit"
        ),

        "validation_status": "",
        "validation_message": "",

        "approval_required": False,
        "approval_status": "",

        "processing_status": "",
        "final_response": "",
    }

    print("\n========== INITIAL STATE ==========")
    print(initial_state)

    result = graph.invoke(initial_state)

    print("\n========== FINAL STATE ==========")
    print(result)