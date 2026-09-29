from forecast_agent import build_graph
from langgraph.types import Command


# ============================================================
# GRAPH
# ============================================================

app = build_graph()


# ============================================================
# THREAD
# ============================================================

config = {
    "configurable": {
        "thread_id": "forecast-investigation-001"
    }
}


# ============================================================
# HUMAN DECISION
# ============================================================

decision = {
    "approved": True,
    "reviewer": "human_reviewer",
    "comment": (
        "Evidence reviewed. "
        "Proceed with business briefing."
    ),
}


# ============================================================
# RESUME GRAPH
# ============================================================

result = app.invoke(
    Command(
        resume=decision
    ),
    config=config,
)


# ============================================================
# OUTPUT
# ============================================================

print(
    "\n"
    "====================================================\n"
    " FINAL BUSINESS BRIEFING\n"
    "===================================================="
)

print(
    result.get(
        "briefing",
        "No briefing generated.",
    )
)