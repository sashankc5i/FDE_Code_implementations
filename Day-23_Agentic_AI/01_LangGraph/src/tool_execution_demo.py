from src.state import ReimbursementState

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END


# =========================================================
# TOOLS
# =========================================================

@tool
def check_reimbursement_policy(
    expense_type: str,
    amount: float,
) -> str:
    """
    Check whether an expense is within the reimbursement policy.
    """

    if expense_type == "Travel" and amount <= 10000:
        return "Expense is within the travel reimbursement policy."

    if expense_type == "Food" and amount <= 3000:
        return "Expense is within the food reimbursement policy."

    return "Expense exceeds the configured reimbursement policy."


@tool
def calculate_reimbursement(
    amount: float,
) -> float:
    """
    Calculate the reimbursement amount.
    """

    # Simulated business rule:
    # reimburse the full approved amount.
    return amount


@tool
def process_payment(
    employee_id: str,
    amount: float,
) -> str:
    """
    Simulate sending the reimbursement payment.
    """

    return (
        f"Payment of ₹{amount:.2f} processed "
        f"for employee {employee_id}."
    )


# =========================================================
# GRAPH NODES
# =========================================================

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


def check_policy(state: ReimbursementState):

    print("→ Checking reimbursement policy")

    policy_result = check_reimbursement_policy.invoke(
        {
            "expense_type": state["expense_type"],
            "amount": state["amount"],
        }
    )

    print(f"  Policy result: {policy_result}")

    return {
        "validation_message": policy_result,
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


def calculate_amount(state: ReimbursementState):

    print("→ Calculating reimbursement amount")

    reimbursement_amount = calculate_reimbursement.invoke(
        {
            "amount": state["amount"],
        }
    )

    print(
        f"  Reimbursement amount: ₹{reimbursement_amount:.2f}"
    )

    return {
        "processing_status": (
            f"Calculated ₹{reimbursement_amount:.2f}"
        ),
    }


def process_payment_node(state: ReimbursementState):

    print("→ Calling payment tool")

    payment_result = process_payment.invoke(
        {
            "employee_id": state["employee_id"],
            "amount": state["amount"],
        }
    )

    print(f"  Payment result: {payment_result}")

    return {
        "processing_status": "processed",
        "final_response": payment_result,
    }


# =========================================================
# GRAPH
# =========================================================

builder = StateGraph(ReimbursementState)

builder.add_node(
    "validate_reimbursement",
    validate_reimbursement,
)

builder.add_node(
    "check_policy",
    check_policy,
)

builder.add_node(
    "determine_approval",
    determine_approval,
)

builder.add_node(
    "calculate_amount",
    calculate_amount,
)

builder.add_node(
    "process_payment",
    process_payment_node,
)


builder.add_edge(
    START,
    "validate_reimbursement",
)

builder.add_edge(
    "validate_reimbursement",
    "check_policy",
)

builder.add_edge(
    "check_policy",
    "determine_approval",
)

builder.add_edge(
    "determine_approval",
    "calculate_amount",
)

builder.add_edge(
    "calculate_amount",
    "process_payment",
)

builder.add_edge(
    "process_payment",
    END,
)


graph = builder.compile()


# =========================================================
# EXECUTION
# =========================================================

if __name__ == "__main__":

    initial_state: ReimbursementState = {

        "employee_id": "EMP-1042",

        "expense_type": "Travel",

        "amount": 4500.00,

        "description": (
            "Flight for client meeting"
        ),

        "validation_status": "",
        "validation_message": "",

        "approval_required": False,
        "approval_status": "",

        "processing_status": "",
        "final_response": "",
    }

    print("\n========== TOOL EXECUTION ==========\n")

    result = graph.invoke(initial_state)

    print("\n========== FINAL RESULT ==========\n")

    print(result)