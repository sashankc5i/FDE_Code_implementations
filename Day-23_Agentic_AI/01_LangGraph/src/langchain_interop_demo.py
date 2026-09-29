import os

from dotenv import load_dotenv

from src.state import ReimbursementState

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, START, END


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
# GRAPH NODES
# =========================================================

def validate_reimbursement(state: ReimbursementState):

    print("→ Validating reimbursement")

    if state["amount"] <= 0:
        return {
            "validation_status": "invalid",
            "validation_message": (
                "Amount must be greater than zero."
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
                "Description is required."
            ),
        }

    return {
        "validation_status": "valid",
        "validation_message": (
            "Reimbursement claim is valid."
        ),
    }


def analyze_with_llm(state: ReimbursementState):

    print("→ Asking LangChain model to analyze claim")

    prompt = f"""
You are a reimbursement policy assistant.

Analyze this reimbursement claim.

Employee ID: {state["employee_id"]}
Expense Type: {state["expense_type"]}
Amount: ₹{state["amount"]}
Description: {state["description"]}

Determine whether this claim appears:
- NORMAL
- NEEDS_REVIEW

Rules:
- Claims above ₹5,000 should normally require review.
- Claims at or below ₹5,000 can normally proceed.
- Suspicious or unclear descriptions should require review.

Return ONLY one word:
NORMAL
or
NEEDS_REVIEW
"""

    response = llm.invoke(
        [
            HumanMessage(content=prompt)
        ]
    )

    decision = response.content.strip().upper()

    print(f"  LLM decision: {decision}")

    return {
        "approval_status": decision,
    }


def route_llm_decision(state: ReimbursementState):

    if state["approval_status"] == "NEEDS_REVIEW":
        return "review"

    return "process"


def process_reimbursement(state: ReimbursementState):

    print("→ Processing reimbursement")

    return {
        "processing_status": "processed",
        "final_response": (
            "Reimbursement processed after LangChain analysis."
        ),
    }


def request_review(state: ReimbursementState):

    print("→ Claim requires review")

    return {
        "processing_status": "review_required",
        "final_response": (
            "Reimbursement requires human review."
        ),
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
    "analyze_with_llm",
    analyze_with_llm,
)

builder.add_node(
    "process_reimbursement",
    process_reimbursement,
)

builder.add_node(
    "request_review",
    request_review,
)


builder.add_edge(
    START,
    "validate_reimbursement",
)

builder.add_edge(
    "validate_reimbursement",
    "analyze_with_llm",
)


builder.add_conditional_edges(
    "analyze_with_llm",
    route_llm_decision,
    {
        "process": "process_reimbursement",
        "review": "request_review",
    },
)


builder.add_edge(
    "process_reimbursement",
    END,
)

builder.add_edge(
    "request_review",
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

    print("\n========== LANGCHAIN + LANGGRAPH ==========\n")

    result = graph.invoke(initial_state)

    print("\n========== FINAL RESULT ==========\n")

    print(result)