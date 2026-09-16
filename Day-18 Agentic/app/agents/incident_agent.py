from app.llm.groq_client import client
from app.config import settings
from app.tools.pipeline_tools import pipeline_status_tool


SYSTEM_PROMPT = """
You are an AI Data Engineering Incident Investigation Agent.

Your job is to investigate data pipeline incidents.

You have access to tools that provide information about
enterprise data pipelines.

Rules:
1. Use tools when you need factual information.
2. Never invent pipeline information.
3. Do not claim a pipeline status without checking the tool.
4. After receiving tool results, analyze them and decide what to do next.
5. If the available evidence is insufficient, say so.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_pipeline_status",
            "description": (
                "Get the current status and latest failure information "
                "for a data pipeline."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pipeline_id": {
                        "type": "string",
                        "description": "The unique pipeline identifier.",
                    }
                },
                "required": ["pipeline_id"],
            },
        },
    }
]


def execute_tool(tool_name: str, arguments: dict) -> dict:

    if tool_name == "get_pipeline_status":
        return pipeline_status_tool(
            arguments["pipeline_id"]
        )

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}",
    }


def run_agent(user_input: str) -> str:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    # No tool requested → return normal answer
    if not message.tool_calls:
        return message.content

    # Process tool calls
    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name

        import json

        arguments = json.loads(
            tool_call.function.arguments
        )

        tool_result = execute_tool(
            tool_name,
            arguments,
        )

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ],
            }
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result),
            }
        )

    # Ask the model to reason over the observation
    final_response = client.chat.completions.create(
        model=settings.groq_model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    return final_response.choices[0].message.content