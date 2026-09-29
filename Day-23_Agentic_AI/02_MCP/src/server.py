from mcp.server import MCPServer

from data import employees, reimbursements, reimbursement_policy

from tools import (
    get_employee,
    get_reimbursement,
    create_reimbursement,
    approve_reimbursement,
    reject_reimbursement,
)


mcp = MCPServer("Reimbursement Server")


# ============================================================
# TOOLS
# ============================================================

mcp.tool()(get_employee)
mcp.tool()(get_reimbursement)
mcp.tool()(create_reimbursement)
mcp.tool()(approve_reimbursement)
mcp.tool()(reject_reimbursement)


# ============================================================
# RESOURCES
# ============================================================

@mcp.resource("employee://{employee_id}")
def employee_resource(employee_id: str) -> dict:
    """Retrieve employee information as an MCP resource."""

    employee = employees.get(employee_id)

    if not employee:
        return {
            "error": f"Employee {employee_id} not found"
        }

    return employee


@mcp.resource("reimbursement://{claim_id}")
def reimbursement_resource(claim_id: str) -> dict:
    """Retrieve reimbursement information as an MCP resource."""

    claim = reimbursements.get(claim_id)

    if not claim:
        return {
            "error": f"Claim {claim_id} not found"
        }

    return claim


@mcp.resource("policy://reimbursement")
def reimbursement_policy_resource() -> dict:
    """Retrieve the reimbursement policy."""

    return reimbursement_policy


# ============================================================
# PROMPTS
# ============================================================

@mcp.prompt()
def reimbursement_review(
    claim_id: str,
    reviewer_id: str,
) -> str:
    """Generate a reimbursement review prompt."""

    return f"""
Review reimbursement claim {claim_id} for reviewer {reviewer_id}.

Follow this review sequence:

1. Retrieve the reimbursement claim.
2. Retrieve the employee information.
3. Check the applicable reimbursement policy.
4. Verify whether the expense is within policy.
5. Identify any missing or suspicious information.
6. Recommend whether the claim should proceed to approval or rejection.

Do not approve or reject the claim automatically.

Provide the reasoning and supporting information
for the reviewer.
"""


# ============================================================
# SERVER ENTRY POINT
# ============================================================

if __name__ == "__main__":
    mcp.run()