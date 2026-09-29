import asyncio
import json
import sys
from pathlib import Path
from typing import Any

from langchain_core.tools import StructuredTool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from mcp import Client, StdioServerParameters
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

CURRENT_DIR = Path(__file__).resolve().parent
SERVER_FILE = CURRENT_DIR / "server.py"

server_parameters = StdioServerParameters(
    command=sys.executable,
    args=[SERVER_FILE.name],
    cwd=str(CURRENT_DIR),
)


# ============================================================
# MCP RESPONSE PARSER
# ============================================================

def parse_tool_result(result) -> dict:
    """Convert an MCP tool result into a Python dictionary."""

    if result.is_error:
        raise RuntimeError(
            f"MCP tool execution failed: {result.content}"
        )

    for item in result.content:
        if getattr(item, "type", None) == "text":
            return json.loads(item.text)

    raise ValueError("No JSON text content found")


# ============================================================
# MCP → LANGGRAPH TOOL ADAPTER
# ============================================================

from pydantic import create_model


def create_mcp_tool(mcp_client: Client, mcp_tool: Any):
    """
    Convert an MCP tool definition into a LangChain StructuredTool.
    """

    schema = mcp_tool.input_schema

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    fields = {}

    for field_name, field_schema in properties.items():

        field_type = str

        if field_schema.get("type") == "integer":
            field_type = int

        elif field_schema.get("type") == "number":
            field_type = float

        elif field_schema.get("type") == "boolean":
            field_type = bool

        default = (
            ...
            if field_name in required
            else None
        )

        fields[field_name] = (
            field_type,
            default,
        )

    args_model = create_model(
        f"{mcp_tool.name.title()}Arguments",
        **fields,
    )

    async def call_mcp_tool(**kwargs):
        result = await mcp_client.call_tool(
            mcp_tool.name,
            kwargs,
        )

        return parse_tool_result(result)

    return StructuredTool.from_function(
        coroutine=call_mcp_tool,
        name=mcp_tool.name,
        description=mcp_tool.description or "",
        args_schema=args_model,
    )


# ============================================================
# LANGGRAPH AGENT
# ============================================================

async def main() -> None:

    async with Client(server_parameters) as mcp_client:

        # ----------------------------------------------------
        # DISCOVER MCP TOOLS
        # ----------------------------------------------------

        tools_result = await mcp_client.list_tools()

        print("\n=== MCP TOOLS DISCOVERED ===")

        langgraph_tools = []

        for mcp_tool in tools_result.tools:

            print(f"- {mcp_tool.name}")

            langgraph_tool = create_mcp_tool(
                mcp_client,
                mcp_tool,
            )

            langgraph_tools.append(langgraph_tool)

        # ----------------------------------------------------
        # LLM
        # ----------------------------------------------------

        model = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
        )

        # ----------------------------------------------------
        # LANGGRAPH
        # ----------------------------------------------------

        agent = create_agent(
        model=model,
        tools=langgraph_tools,
)

        # ----------------------------------------------------
        # USER REQUEST
        # ----------------------------------------------------

        request = (
    "Approve reimbursement claim CLM1001. "
    "The authorized approver is MGR001. "
    "First retrieve the claim and employee information. "
    "If the claim is currently PENDING, approve it using "
    "MGR001 as the approver. "
    "Then retrieve the claim again and report its final status."
)

        print("\n=== USER REQUEST ===")
        print(request)

        # ----------------------------------------------------
        # EXECUTE AGENT
        # ----------------------------------------------------

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": request,
                    }
                ]
            }
        )

        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        print("\n=== AGENT RESPONSE ===")

        final_message = result["messages"][-1]

        print(final_message.content)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())