import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from app.config import settings
from app.llm.groq_client import client

from app.agents.log_agent import investigate_logs
from app.agents.data_agent import investigate_data
from app.agents.deployment_agent import investigate_deployment


SUPERVISOR_PROMPT = """
You are an AI Data Engineering Incident Supervisor.

Your job is to determine which specialist investigations
are relevant to an incident.

Available specialists:

1. log
   Investigates pipeline execution logs.

2. data
   Investigates source table schema and data-related evidence.

3. deployment
   Investigates recent deployment information.

Rules:

- Only select specialists from the available list.
- Do not invent specialist names.
- Select only specialists relevant to the evidence.
- If the failure involves a missing or unresolved column,
  select log and data.
- If the failure appears related to deployment,
  select log and deployment.
- If the failure appears infrastructure-related,
  select log.
- Prefer independent evidence sources.
- Return JSON only.

Required format:

{
    "investigations": ["log", "data"],
    "reason": "short explanation"
}
"""


AVAILABLE_INVESTIGATIONS = {
    "log",
    "data",
    "deployment",
}


def choose_investigations(
    incident_description: str,
) -> dict:

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[
            {
                "role": "system",
                "content": SUPERVISOR_PROMPT,
            },
            {
                "role": "user",
                "content": incident_description,
            },
        ],
        response_format={
            "type": "json_object"
        },
    )

    content = response.choices[0].message.content

    decision = json.loads(content)

    requested = decision.get(
        "investigations",
        [],
    )

    # Application-level validation.
    valid = [
        investigation
        for investigation in requested
        if investigation in AVAILABLE_INVESTIGATIONS
    ]

    return {
        "investigations": valid,
        "reason": decision.get(
            "reason",
            "",
        ),
    }


def run_parallel_investigation(
    pipeline_id: str,
    table_name: str | None = None,
    incident_description: str = "",
) -> dict:

    decision = choose_investigations(
        incident_description
    )

    investigations = decision["investigations"]

    results = []

    with ThreadPoolExecutor(
        max_workers=len(investigations) or 1
    ) as executor:

        futures = {}

        if "log" in investigations:
            futures[
                executor.submit(
                    investigate_logs,
                    pipeline_id,
                )
            ] = "log_agent"

        if "data" in investigations and table_name:
            futures[
                executor.submit(
                    investigate_data,
                    table_name,
                )
            ] = "data_agent"

        if "deployment" in investigations:
            futures[
                executor.submit(
                    investigate_deployment,
                    pipeline_id,
                )
            ] = "deployment_agent"

        for future in as_completed(futures):

            agent_name = futures[future]

            try:
                result = future.result()

            except Exception as exc:

                result = {
                    "agent": agent_name,
                    "status": "FAILED",
                    "findings": [],
                    "confidence": 0.0,
                    "error": str(exc),
                }

            results.append(result)

    return {
        "status": "COMPLETED",
        "decision": decision,
        "investigations": results,
    }