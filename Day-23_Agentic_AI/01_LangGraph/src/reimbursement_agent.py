import os
from typing import Literal

from dotenv import load_dotenv

from src.state import ReimbursementState

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# LANGCHAIN MODEL
# =========================================================

llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    ),
    temperature=0,
)


# =========================================================
# BUSINESS TOOLS
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

    return amount


@tool
def process_payment(
    employee_id: str,
    amount: float,
) -> str:
    """
    Simulate processing the reimbursement payment.
    """

    return (
        f"Payment of ₹{amount:.2f} processed "
        f"for employee {employee_id}."
    )


@tool
def notify_employee(
    employee_id: str,
    message: str,
) -> str:
    """
    Simulate sending a reimbursement notification.
    """

    return (
        f"Notification sent to {employee_id}: {message}"
    )


# =========================================================
# NODE 1 — VALIDATION
# =========================================================

def validate_reimbursement(
    state: ReimbursementState,
):
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


# =========================================================
# ROUTING — VALIDATION
# =========================================================

def route_validation(
    state: ReimbursementState,
) -> Literal["valid", "invalid"]:

    if state["validation_status"] == "valid":
        return "valid"

    return "invalid"


# =========================================================
# NODE 2 — INVALID CLAIM
# =========================================================

def reject_invalid_claim(
    state: ReimbursementState,
):

    print("→ Rejecting invalid reimbursement")

    notification = notify_employee.invoke(
        {
            "employee_id": state["employee_id"],
            "message": (
                f"Your reimbursement was rejected: "
                f"{state['validation_message']}"
            ),
        }
    )

    print(f"  {notification}")

    return {
        "processing_status": "rejected",
        "final_response": (
            f"Reimbursement rejected: "
            f"{state['validation_message']}"
        ),
    }


# =========================================================
# NODE 3 — POLICY TOOL
# =========================================================

def check_policy(
    state: ReimbursementState,
):

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


# =========================================================
# NODE 4 — LANGCHAIN LLM ANALYSIS
# =========================================================

def analyze_claim(
    state: ReimbursementState,
):

    print("→ Asking LangChain model to analyze claim")

    prompt = f"""
You are a reimbursement policy analysis assistant.

Analyze the following reimbursement claim.

Employee ID:
{state["employee_id"]}

Expense type:
{state["expense_type"]}

Amount:
₹{state["amount"]}

Description:
{state["description"]}

Policy result:
{state["validation_message"]}

Decision rules:

1. If the claim is ordinary and within policy,
   classify it as NORMAL.

2. If the claim is unusually large, unclear,
   suspicious, or requires managerial judgment,
   classify it as NEEDS_REVIEW.

3. Any claim above ₹5,000 should be classified
   as NEEDS_REVIEW.

Return ONLY one of these exact values:

NORMAL
NEEDS_REVIEW
"""

    response = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    decision = response.content.strip().upper()

    if "NEEDS_REVIEW" in decision:
        decision = "NEEDS_REVIEW"
    else:
        decision = "NORMAL"

    print(f"  LLM decision: {decision}")

    return {
        "approval_status": decision,
    }


# =========================================================
# ROUTING — LLM DECISION
# =========================================================

def route_llm_decision(
    state: ReimbursementState,
) -> Literal["process", "human_approval"]:

    if state["approval_status"] == "NEEDS_REVIEW":
        return "human_approval"

    return "process"


# =========================================================
# NODE 5 — CALCULATE REIMBURSEMENT
# =========================================================

def calculate_amount(
    state: ReimbursementState,
):

    print("→ Calculating reimbursement amount")

    reimbursement_amount = calculate_reimbursement.invoke(
        {
            "amount": state["amount"],
        }
    )

    print(
        f"  Reimbursement amount: "
        f"₹{reimbursement_amount:.2f}"
    )

    return {
        "processing_status": (
            f"Calculated ₹{reimbursement_amount:.2f}"
        ),
    }


# =========================================================
# NODE 6 — HUMAN APPROVAL
# =========================================================

def human_approval(
    state: ReimbursementState,
):

    print("→ Waiting for human approval")

    decision = interrupt(
        {
            "message": (
                "Human approval required for reimbursement."
            ),
            "employee_id": state["employee_id"],
            "amount": state["amount"],
            "expense_type": state["expense_type"],
            "description": state["description"],
        }
    )

    print(
        f"→ Human decision received: {decision}"
    )

    if decision == "approved":

        return {
            "approval_status": "approved",
        }

    return {
        "approval_status": "rejected",
    }


# =========================================================
# ROUTING — HUMAN DECISION
# =========================================================

def route_human_decision(
    state: ReimbursementState,
) -> Literal["process", "reject"]:

    if state["approval_status"] == "approved":
        return "process"

    return "reject"


# =========================================================
# NODE 7 — PROCESS PAYMENT
# =========================================================

def process_reimbursement(
    state: ReimbursementState,
):

    print("→ Processing reimbursement")

    payment_result = process_payment.invoke(
        {
            "employee_id": state["employee_id"],
            "amount": state["amount"],
        }
    )

    print(f"  {payment_result}")

    notification = notify_employee.invoke(
        {
            "employee_id": state["employee_id"],
            "message": (
                "Your reimbursement has been approved "
                "and processed."
            ),
        }
    )

    print(f"  {notification}")

    return {
        "processing_status": "processed",
        "final_response": payment_result,
    }


# =========================================================
# NODE 8 — REJECT AFTER HUMAN REVIEW
# =========================================================

def reject_after_review(
    state: ReimbursementState,
):

    print("→ Rejecting reimbursement after human review")

    notification = notify_employee.invoke(
        {
            "employee_id": state["employee_id"],
            "message": (
                "Your reimbursement request was "
                "rejected after human review."
            ),
        }
    )

    print(f"  {notification}")

    return {
        "processing_status": "rejected",
        "final_response": (
            "Reimbursement rejected after human review."
        ),
    }


# =========================================================
# GRAPH CONSTRUCTION
# =========================================================

builder = StateGraph(ReimbursementState)


builder.add_node(
    "validate_reimbursement",
    validate_reimbursement,
)

builder.add_node(
    "reject_invalid_claim",
    reject_invalid_claim,
)

builder.add_node(
    "check_policy",
    check_policy,
)

builder.add_node(
    "analyze_claim",
    analyze_claim,
)

builder.add_node(
    "calculate_amount",
    calculate_amount,
)

builder.add_node(
    "human_approval",
    human_approval,
)

builder.add_node(
    "process_reimbursement",
    process_reimbursement,
)

builder.add_node(
    "reject_after_review",
    reject_after_review,
)


# =========================================================
# GRAPH EDGES
# =========================================================

builder.add_edge(
    START,
    "validate_reimbursement",
)


builder.add_conditional_edges(
    "validate_reimbursement",
    route_validation,
    {
        "valid": "check_policy",
        "invalid": "reject_invalid_claim",
    },
)


builder.add_edge(
    "check_policy",
    "analyze_claim",
)


builder.add_conditional_edges(
    "analyze_claim",
    route_llm_decision,
    {
        "process": "calculate_amount",
        "human_approval": "human_approval",
    },
)


builder.add_conditional_edges(
    "human_approval",
    route_human_decision,
    {
        "process": "calculate_amount",
        "reject": "reject_after_review",
    },
)


builder.add_edge(
    "calculate_amount",
    "process_reimbursement",
)


builder.add_edge(
    "process_reimbursement",
    END,
)

builder.add_edge(
    "reject_invalid_claim",
    END,
)

builder.add_edge(
    "reject_after_review",
    END,
)


# =========================================================
# PERSISTENCE
# =========================================================

memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# =========================================================
# STATE FACTORY
# =========================================================

def create_state(
    employee_id: str,
    expense_type: str,
    amount: float,
    description: str,
) -> ReimbursementState:

    return {
        "employee_id": employee_id,
        "expense_type": expense_type,
        "amount": amount,
        "description": description,

        "validation_status": "",
        "validation_message": "",

        "approval_required": False,
        "approval_status": "",

        "processing_status": "",
        "final_response": "",
    }


# =========================================================
# END-TO-END TEST RUNNER
# =========================================================

def run_test_case(
    name: str,
    thread_id: str,
    state: ReimbursementState,
    human_decision: str | None = None,
):

    print("\n")
    print("=" * 70)
    print(name)
    print("=" * 70)

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    print("\n--- FIRST EXECUTION ---\n")

    result = graph.invoke(
        state,
        config,
    )

    print("\nCURRENT RESULT:")
    print(result)

    # -----------------------------------------------------
    # HUMAN APPROVAL PATH
    # -----------------------------------------------------

    if "__interrupt__" in result:

        print("\n--- WORKFLOW PAUSED ---\n")

        snapshot = graph.get_state(config)

        print(
            f"Next node: {snapshot.next}"
        )

        print(
            f"Checkpoint thread: "
            f"{thread_id}"
        )

        print("\n--- HUMAN DECISION ---\n")

        print(
            f"Decision: {human_decision}"
        )

        print("\n--- RESUMING WORKFLOW ---\n")

        final_result = graph.invoke(
            Command(
                resume=human_decision
            ),
            config,
        )

        print("\nFINAL RESULT:")
        print(final_result)

        return final_result

    print("\n--- WORKFLOW COMPLETED ---\n")

    print("FINAL RESULT:")
    print(result)

    return result


# =========================================================
# END-TO-END TESTS
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # TEST 1 — NORMAL AUTO PROCESS
    # -----------------------------------------------------

    run_test_case(
        name="TEST 1 — NORMAL AUTO PROCESS",
        thread_id="reimbursement-final-001",
        state=create_state(
            employee_id="EMP-2001",
            expense_type="Food",
            amount=2500.00,
            description="Client dinner",
        ),
    )


    # -----------------------------------------------------
    # TEST 2 — HUMAN APPROVAL → APPROVED
    # -----------------------------------------------------

    run_test_case(
        name="TEST 2 — HUMAN APPROVAL → APPROVED",
        thread_id="reimbursement-final-002",
        state=create_state(
            employee_id="EMP-2002",
            expense_type="Travel",
            amount=8500.00,
            description="Flight for client meeting",
        ),
        human_decision="approved",
    )


    # -----------------------------------------------------
    # TEST 3 — HUMAN APPROVAL → REJECTED
    # -----------------------------------------------------

    run_test_case(
        name="TEST 3 — HUMAN APPROVAL → REJECTED",
        thread_id="reimbursement-final-003",
        state=create_state(
            employee_id="EMP-2003",
            expense_type="Travel",
            amount=8500.00,
            description="Flight for client meeting",
        ),
        human_decision="rejected",
    )


    # -----------------------------------------------------
    # TEST 4 — INVALID CLAIM
    # -----------------------------------------------------

    run_test_case(
        name="TEST 4 — INVALID CLAIM",
        thread_id="reimbursement-final-004",
        state=create_state(
            employee_id="EMP-2004",
            expense_type="Travel",
            amount=-500.00,
            description="Invalid reimbursement",
        ),
    )