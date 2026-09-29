from src.state import ReimbursementState

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END


def validate_reimbursement(state: ReimbursementState):
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


# Create a checkpointer.
memory = MemorySaver()

# Compile the graph with persistence enabled.
graph = builder.compile(
    checkpointer=memory
)


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

    config = {
        "configurable": {
            "thread_id": "reimbursement-EMP-1042-001"
        }
    }

    print("\n========== FIRST EXECUTION ==========")

    result = graph.invoke(
        initial_state,
        config=config,
    )

    print(result)

    print("\n========== SAVED STATE ==========")

    saved_state = graph.get_state(config)

    print(saved_state)