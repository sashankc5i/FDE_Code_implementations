import json

from app.config import settings
from app.llm.groq_client import client

from app.tools.pipeline_tools import (
    pipeline_search_tool,
    pipeline_status_tool,
    pipeline_logs_tool,
    table_schema_tool,
)

from app.models.incident_state import IncidentState

from app.workflows.state_manager import (
    add_observation,
    record_action,
    update_state,
    record_error,
)

from app.agents.failure_classifier import classify_failure


SYSTEM_PROMPT = """
You are an AI Data Engineering Incident Investigation Agent.

Your job is to investigate data pipeline incidents.

You have access only to the tools explicitly provided
by the application.

Investigation rules:

1. Use tools when factual information is required.

2. Never invent evidence.

3. Never assume an internal pipeline ID.

4. If the user gives a human-readable pipeline name,
   use find_pipeline to obtain the canonical pipeline ID.

5. Once find_pipeline returns a canonical pipeline ID,
   do NOT call find_pipeline again for the same pipeline.

6. Use the canonical pipeline ID for subsequent pipeline tools.

7. Treat every tool result as an observation.

8. Tool failures are observations too.

9. Do not guess table names or infrastructure identifiers.

10. Use information from previous tool results to determine
    the next investigation step.

11. Do not repeat a tool call with the same arguments.

12. If the logs identify a source table relevant to the
    failure, investigate that table using get_table_schema.

13. Once sufficient evidence exists to identify the likely
    root cause, stop calling tools and provide the answer.

14. If evidence is insufficient and no available tool can
    provide the missing evidence, stop and explain what
    information is missing.

15. Never fabricate a root cause.

16. Distinguish clearly between:
    - observed facts
    - likely root cause
    - unresolved underlying cause

17. Never claim access to a system unless an available
    tool actually returned information from that system.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "find_pipeline",
            "description": (
                "Find a data pipeline using its human-readable name "
                "and return its canonical pipeline ID. "
                "Use this only when the canonical pipeline ID is unknown."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Human-readable pipeline name.",
                    }
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pipeline_status",
            "description": (
                "Get the current status and latest failure information "
                "for a data pipeline using its canonical pipeline ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pipeline_id": {
                        "type": "string",
                        "description": "Canonical pipeline ID.",
                    }
                },
                "required": ["pipeline_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pipeline_logs",
            "description": (
                "Retrieve execution logs for a data pipeline. "
                "Use this to investigate the cause of a pipeline failure."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pipeline_id": {
                        "type": "string",
                        "description": "Canonical pipeline ID.",
                    }
                },
                "required": ["pipeline_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_table_schema",
            "description": (
                "Retrieve the current column schema of a source table. "
                "Use this when investigating schema-related failures "
                "and only when the table name is supported by previous "
                "tool observations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Name of the table to inspect.",
                    }
                },
                "required": ["table_name"],
            },
        },
    },
]


def execute_tool(
    tool_name: str,
    arguments: dict,
) -> dict:

    if tool_name == "find_pipeline":
        return pipeline_search_tool(
            arguments["name"]
        )

    if tool_name == "get_pipeline_status":
        return pipeline_status_tool(
            arguments["pipeline_id"]
        )

    if tool_name == "get_pipeline_logs":
        return pipeline_logs_tool(
            arguments["pipeline_id"]
        )

    if tool_name == "get_table_schema":
        return table_schema_tool(
            arguments["table_name"]
        )

    return {
        "success": False,
        "error": f"Unknown tool: {tool_name}",
    }


def run_agent(
    user_input: str,
    state: IncidentState,
    max_iterations: int = 6,
):
    """
    Run or resume an incident investigation.

    The IncidentState is persisted after important changes
    through the state manager.
    """

    # ---------------------------------------------------------
    # STATE: START -> INVESTIGATING
    # ---------------------------------------------------------

    if state.current_state == "START":
        update_state(
            state,
            "INVESTIGATING",
        )

    elif state.current_state in {
        "SUCCESS",
        "FAILED",
        "ESCALATED",
    }:
        return (
            f"Incident is already in terminal state: "
            f"{state.current_state}"
        )

    # ---------------------------------------------------------
    # LLM MESSAGE HISTORY
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # AGENT LOOP
    # ---------------------------------------------------------

    for _ in range(max_iterations):

        state.llm_iterations += 1

        print(
            f"\n--- Agent iteration "
            f"{state.llm_iterations} ---"
        )

        try:

            response = client.chat.completions.create(
                model=settings.groq_model,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
            )

        except Exception as exc:

            error_message = (
                f"LLM execution failed: {str(exc)}"
            )

            record_error(
                state,
                error_message,
            )

            state.requires_human = True

            update_state(
                state,
                "ESCALATED",
            )

            return (
                "The agent encountered an LLM execution "
                "error and the incident has been escalated."
            )

        message = response.choices[0].message

        print(
            f"Finish reason: "
            f"{response.choices[0].finish_reason}"
        )

        print(
            "Tool calls:",
            message.tool_calls,
        )

        # -----------------------------------------------------
        # AGENT DECIDES TO FINISH
        # -----------------------------------------------------

        if not message.tool_calls:

            failure_type = classify_failure(state)

            state.failure_type = failure_type

            update_state(
                state,
                "CLASSIFYING",
            )

            return message.content

        # -----------------------------------------------------
        # ADD ASSISTANT TOOL-CALL MESSAGE
        # -----------------------------------------------------

        messages.append(message)

        # -----------------------------------------------------
        # EXECUTE TOOL CALLS
        # -----------------------------------------------------

        for tool_call in message.tool_calls:

            state.tool_calls += 1

            tool_name = tool_call.function.name

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError as exc:

                error_message = (
                    f"Invalid tool arguments for "
                    f"{tool_name}: {str(exc)}"
                )

                record_error(
                    state,
                    error_message,
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            {
                                "success": False,
                                "error": error_message,
                            }
                        ),
                    }
                )

                continue

            print(
                f"Executing tool: {tool_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            # -------------------------------------------------
            # EXECUTE TOOL
            # -------------------------------------------------

            result = execute_tool(
                tool_name,
                arguments,
            )

            print(
                f"Tool result: {result}"
            )

            # -------------------------------------------------
            # RECORD ACTION
            # -------------------------------------------------

            record_action(
                state,
                f"{tool_name}({arguments})",
            )

            # -------------------------------------------------
            # RECORD OBSERVATION
            # -------------------------------------------------

            add_observation(
                state,
                tool_name,
                result,
            )

            # -------------------------------------------------
            # RETURN TOOL RESULT TO LLM
            # -------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    # ---------------------------------------------------------
    # MAX ITERATIONS REACHED
    # ---------------------------------------------------------

    state.requires_human = True

    record_error(
        state,
        "Maximum investigation iterations exceeded.",
    )

    update_state(
        state,
        "ESCALATED",
    )

    return (
        "Investigation exceeded the allowed "
        "iteration limit and has been escalated."
    )