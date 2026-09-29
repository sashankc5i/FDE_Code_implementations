import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters


# ============================================================
# SERVER CONFIGURATION
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent
SERVER_FILE = CURRENT_DIR / "server.py"

server_parameters = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_FILE.name],
    cwd=str(CURRENT_DIR),
)


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_tool_result(result) -> dict:
    """
    Convert an MCP CallToolResult into a normal Python dictionary.
    """

    if result.is_error:
        raise RuntimeError(
            f"MCP tool execution failed: {result.content}"
        )

    for item in result.content:
        if getattr(item, "type", None) == "text":
            return json.loads(item.text)

    raise ValueError("No JSON text content found in MCP response")


# ============================================================
# MCP CLIENT
# ============================================================

async def main() -> None:

    async with Client(server_parameters) as client:

        print("\n=== MCP SERVER INFORMATION ===")

        if client.server_info:
            print(f"Name: {client.server_info.name}")
            print(f"Version: {client.server_info.version}")

        print(f"Protocol: {client.protocol_version}")

        # ----------------------------------------------------
        # TOOL DISCOVERY
        # ----------------------------------------------------

        print("\n=== DISCOVERED TOOLS ===")

        tools_result = await client.list_tools()

        for tool in tools_result.tools:
            print(f"- {tool.name}")
            print(f"  Description: {tool.description}")

        # ----------------------------------------------------
        # GET EMPLOYEE
        # ----------------------------------------------------

        print("\n=== CALL: get_employee ===")

        employee_result = await client.call_tool(
            "get_employee",
            {
                "employee_id": "EMP001"
            },
        )

        employee = parse_tool_result(employee_result)

        print(employee)

        # ----------------------------------------------------
        # GET REIMBURSEMENT
        # ----------------------------------------------------

        print("\n=== CALL: get_reimbursement ===")

        reimbursement_result = await client.call_tool(
            "get_reimbursement",
            {
                "claim_id": "CLM1001"
            },
        )

        reimbursement = parse_tool_result(
            reimbursement_result
        )

        print(reimbursement)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())