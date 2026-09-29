from src.state import ReimbursementState

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command


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


def route_approval(state: ReimbursementState):
    if state["approval_required"]:
        return "human_approval"

    return "auto_process"


def human_approval(state: ReimbursementState):
    print("→ Waiting for human approval")

    decision = interrupt(
        {
            "message": "Human approval required for reimbursement.",
            "employee_id": state["employee_id"],
            "amount": state["amount"],
            "expense_type": state["expense_type"],
            "description": state["description"],
        }
    )

    print(f"→ Human decision received: {decision}")

    if decision == "approved":
        return {
            "approval_status": "approved",
        }

    return {
        "approval_status": "rejected",
    }


def auto_process(state: ReimbursementState):
    print("→ Automatically processing reimbursement")

    return {
        "processing_status": "processed",
        "final_response": (
            "Reimbursement automatically processed."
        ),
    }


def route_human_decision(state: ReimbursementState):
    if state["approval_status"] == "approved":
        return "process"

    return "reject"


def process_reimbursement(state: ReimbursementState):
    print("→ Processing approved reimbursement")

    return {
        "processing_status": "processed",
        "final_response": (
            "Reimbursement approved and processed."
        ),
    }


def reject_reimbursement(state: ReimbursementState):
    print("→ Rejecting reimbursement")

    return {
        "processing_status": "rejected",
        "final_response": (
            "Reimbursement request was rejected."
        ),
    }


# ---------------------------------------------------------
# BUILD GRAPH
# ---------------------------------------------------------

builder = StateGraph(ReimbursementState)

builder.add_node(
    "validate_reimbursement",
    validate_reimbursement,
)

builder.add_node(
    "determine_approval",
    determine_approval,
)

builder.add_node(
    "human_approval",
    human_approval,
)

builder.add_node(
    "auto_process",
    auto_process,
)

builder.add_node(
    "process_reimbursement",
    process_reimbursement,
)

builder.add_node(
    "reject_reimbursement",
    reject_reimbursement,
)


builder.add_edge(
    START,
    "validate_reimbursement",
)

builder.add_edge(
    "validate_reimbursement",
    "determine_approval",
)


builder.add_conditional_edges(
    "determine_approval",
    route_approval,
    {
        "human_approval": "human_approval",
        "auto_process": "auto_process",
    },
)


builder.add_conditional_edges(
    "human_approval",
    route_human_decision,
    {
        "process": "process_reimbursement",
        "reject": "reject_reimbursement",
    },
)


builder.add_edge(
    "auto_process",
    END,
)

builder.add_edge(
    "process_reimbursement",
    END,
)

builder.add_edge(
    "reject_reimbursement",
    END,
)


# ---------------------------------------------------------
# PERSISTENCE
# ---------------------------------------------------------

memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

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
            "thread_id": "reimbursement-EMP-1042-002"
        }
    }


    # -----------------------------------------------------
    # FIRST EXECUTION
    # -----------------------------------------------------

    print("\n========== FIRST EXECUTION ==========\n")

    result = graph.invoke(
        initial_state,
        config,
    )

    print("\nGRAPH RESULT:")
    print(result)


    # -----------------------------------------------------
    # CHECK PAUSED STATE
    # -----------------------------------------------------

    print("\n========== CURRENT STATE ==========\n")

    snapshot = graph.get_state(config)

    print(snapshot)

    print("\nNEXT:")
    print(snapshot.next)


    # -----------------------------------------------------
    # HUMAN DECISION
    # -----------------------------------------------------

    print("\n========== HUMAN APPROVAL ==========\n")

    human_decision = "approved"

    print(
        f"Human decision: {human_decision}"
    )


    # -----------------------------------------------------
    # RESUME GRAPH
    # -----------------------------------------------------

    print("\n========== RESUMING GRAPH ==========\n")

    final_result = graph.invoke(
        Command(
            resume=human_decision
        ),
        config,
    )

    print("\nFINAL RESULT:")
    print(final_result)