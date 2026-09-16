from app.safety.policies import (
    READ,
    LOW_RISK_WRITE,
    HIGH_RISK_WRITE,
    DESTRUCTIVE,
    TOOL_RISK,
)


def evaluate_action(tool_name: str) -> dict:

    risk = TOOL_RISK.get(tool_name)

    if risk is None:
        return {
            "allowed": False,
            "risk": "UNKNOWN",
            "requires_human": True,
            "reason": (
                f"Tool '{tool_name}' is not "
                "registered in the safety policy."
            ),
        }

    if risk == READ:
        return {
            "allowed": True,
            "risk": READ,
            "requires_human": False,
            "reason": "Read-only operation.",
        }

    if risk == LOW_RISK_WRITE:
        return {
            "allowed": True,
            "risk": LOW_RISK_WRITE,
            "requires_human": False,
            "reason": "Low-risk controlled write.",
        }

    if risk == HIGH_RISK_WRITE:
        return {
            "allowed": False,
            "risk": HIGH_RISK_WRITE,
            "requires_human": True,
            "reason": (
                "High-risk operation requires "
                "human approval."
            ),
        }

    if risk == DESTRUCTIVE:
        return {
            "allowed": False,
            "risk": DESTRUCTIVE,
            "requires_human": True,
            "reason": (
                "Destructive operation requires "
                "explicit human approval."
            ),
        }

    return {
        "allowed": False,
        "risk": "UNKNOWN",
        "requires_human": True,
        "reason": "Unknown policy state.",
    }