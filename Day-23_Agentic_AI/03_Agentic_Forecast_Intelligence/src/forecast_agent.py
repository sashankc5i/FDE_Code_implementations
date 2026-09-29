import json
from typing import Any, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from src.forecast_monitor import monitor_forecast
from src.driver_analysis import investigate_drivers
from src.trend_analysis import analyze_revenue_trend
from src.external_signals import analyze_external_signals
from src.scenario_analysis import run_pipeline_recovery_scenario
from src.evidence import build_forecast_evidence


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# ============================================================
# STATE
# ============================================================

class ForecastState(TypedDict, total=False):

    period: str
    region: str
    segment: str

    forecast_monitoring: dict
    driver_analysis: dict
    trend_analysis: dict
    market_signals: dict
    scenario_analysis: dict

    evidence: list
    hypotheses: list

    prioritized_signals: list
    signal_assessment: list

    human_review: dict

    recommendations: list
    business_briefing: str


# ============================================================
# NODE 1 — INITIALIZE
# ============================================================

def initialize_investigation(
    state: ForecastState,
) -> ForecastState:

    return {
        "period": state["period"],
        "region": state["region"],
        "segment": state["segment"],
    }


# ============================================================
# NODE 2 — FORECAST MONITORING
# ============================================================

def analyze_forecast(
    state: ForecastState,
) -> ForecastState:

    df = monitor_forecast()

    filtered = df[
        (df["period"] == state["period"])
        & (df["region"] == state["region"])
        & (df["segment"] == state["segment"])
    ]

    if filtered.empty:

        return {
            "forecast_monitoring": {
                "available": False,
                "message": "No forecast record found.",
            }
        }

    row = filtered.iloc[0]

    return {
        "forecast_monitoring": {
            "available": True,
            "period": state["period"],
            "region": state["region"],
            "segment": state["segment"],
            "forecast_revenue": float(
                row["forecast_revenue"]
            ),
            "actual_revenue": float(
                row["actual_revenue"]
            ),
            "variance": float(
                row["variance"]
            ),
            "variance_pct": float(
                row["variance_pct"]
            ),
            "investigation_required": bool(
                row["investigation_required"]
            ),
        }
    }


# ============================================================
# NODE 3 — DRIVER ANALYSIS
# ============================================================

def analyze_drivers(
    state: ForecastState,
) -> ForecastState:

    result = investigate_drivers(
        period=state["period"],
        region=state["region"],
        segment=state["segment"],
    )

    return {
        "driver_analysis": result
    }


# ============================================================
# NODE 4 — TREND ANALYSIS
# ============================================================

def analyze_trends(
    state: ForecastState,
) -> ForecastState:

    result = analyze_revenue_trend(
        period=state["period"],
        region=state["region"],
        segment=state["segment"],
    )

    return {
        "trend_analysis": result
    }


# ============================================================
# NODE 5 — MARKET SIGNALS
# ============================================================

def analyze_market_signals(
    state: ForecastState,
) -> ForecastState:

    result = analyze_external_signals(
        period=state["period"],
        region=state["region"],
    )

    return {
        "market_signals": result
    }


# ============================================================
# NODE 6 — SCENARIO
# ============================================================

def analyze_scenario(
    state: ForecastState,
) -> ForecastState:

    result = run_pipeline_recovery_scenario(
        period=state["period"],
        region=state["region"],
        segment=state["segment"],
        recovery_pct=0.25,
    )

    return {
        "scenario_analysis": result
    }

# ============================================================
# NODE 7 — EVIDENCE
# ============================================================

def consolidate_evidence(
    state: ForecastState,
) -> ForecastState:

    result = build_forecast_evidence(
        period=state["period"],
        region=state["region"],
        segment=state["segment"],
    )

    if isinstance(result, dict):

        evidence = result.get(
            "evidence",
            result,
        )

    else:

        evidence = result

    return {
        "evidence": evidence
    }


# ============================================================
# NODE 8 — HYPOTHESES
# ============================================================

def generate_hypotheses(
    state: ForecastState,
) -> ForecastState:

    forecast = state.get(
        "forecast_monitoring",
        {}
    )

    drivers = state.get(
        "driver_analysis",
        {}
    )

    trend = state.get(
        "trend_analysis",
        {}
    )

    market = state.get(
        "market_signals",
        {}
    )

    prompt = f"""
You are investigating a business forecast deviation.

Forecast:
{forecast}

Driver analysis:
{drivers}

Revenue trend:
{trend}

External market signals:
{market}

Evidence:
{state.get("evidence", [])}

Generate up to three plausible hypotheses.

Rules:

1. Hypotheses must be evidence-backed.
2. Do not claim causality.
3. Explicitly describe them as hypotheses.
4. Do not invent facts.
5. Do not treat LOW signals as major drivers.

Return ONLY valid JSON.

Format:

[
  {{
    "hypothesis": "...",
    "supporting_evidence": ["EV001"],
    "confidence": "HIGH"
  }}
]
"""

    response = llm.invoke(
        prompt
    )

    raw = response.content.strip()

    try:
        hypotheses = json.loads(raw)

    except json.JSONDecodeError:
        hypotheses = []

    if not isinstance(
        hypotheses,
        list
    ):
        hypotheses = []

    return {
        "hypotheses": hypotheses
    }


# ============================================================
# NODE 9 — STRUCTURED SIGNAL PRIORITIZATION
# ============================================================

def prioritize_signals(
    state: ForecastState,
) -> ForecastState:

    forecast_monitoring = state.get(
        "forecast_monitoring",
        {}
    )

    investigation_required = bool(
        forecast_monitoring.get(
            "investigation_required",
            False
        )
    )

    evidence = state.get(
        "evidence",
        []
    )

    # --------------------------------------------------------
    # Critical guardrail:
    # No material forecast investigation means no material
    # business signal.
    # --------------------------------------------------------

    if not investigation_required:

        return {
            "prioritized_signals": [],
            "signal_assessment": [],
        }

    prompt = f"""
You are evaluating business signals from a forecast investigation.

Forecast monitoring:
{forecast_monitoring}

Driver analysis:
{state.get("driver_analysis", {})}

Revenue trend:
{state.get("trend_analysis", {})}

External signals:
{state.get("market_signals", {})}

Evidence:
{evidence}

Allowed signal names:

- revenue_deterioration
- pipeline_deterioration
- customer_churn
- external_demand
- pricing

Rules:

1. Only identify signals supported by evidence.
2. Do not invent signals.
3. HIGH = strong evidence of material impact.
4. MEDIUM = meaningful evidence deserving attention.
5. LOW = supporting or weak evidence.
6. Do not infer causality.
7. LOW pricing must not become a major driver.
8. External demand must have supporting evidence.
9. Revenue deterioration must be supported by forecast evidence.
10. Pipeline deterioration must be supported by pipeline evidence.
11. Customer churn must be supported by customer-health evidence.

Return ONLY valid JSON.

Format:

[
  {{
    "signal": "pipeline_deterioration",
    "detected": true,
    "priority": "HIGH",
    "evidence_ids": ["EV002"],
    "reason": "Pipeline declined materially."
  }}
]

If no material signals exist:

[]
"""

    response = llm.invoke(
        prompt
    )

    raw = response.content.strip()

    try:
        parsed = json.loads(raw)

    except json.JSONDecodeError:
        parsed = []

    if not isinstance(
        parsed,
        list
    ):
        parsed = []

    valid_signal_names = {
        "revenue_deterioration",
        "pipeline_deterioration",
        "customer_churn",
        "external_demand",
        "pricing",
    }

    valid_evidence_ids = {
        item.get("evidence_id")
        for item in evidence
        if isinstance(item, dict)
        and item.get("evidence_id")
    }

    validated = []

    for item in parsed:

        if not isinstance(
            item,
            dict
        ):
            continue

        signal = item.get(
            "signal"
        )

        if signal not in valid_signal_names:
            continue

        priority = str(
            item.get(
                "priority",
                "LOW"
            )
        ).upper()

        if priority not in {
            "HIGH",
            "MEDIUM",
            "LOW",
        }:
            priority = "LOW"

        evidence_ids = item.get(
            "evidence_ids",
            []
        )

        if not isinstance(
            evidence_ids,
            list
        ):
            evidence_ids = []

        evidence_ids = [
            evidence_id
            for evidence_id in evidence_ids
            if evidence_id
            in valid_evidence_ids
        ]

        validated.append(
            {
                "signal": signal,
                "detected": bool(
                    item.get(
                        "detected",
                        False
                    )
                ),
                "priority": priority,
                "evidence_ids": evidence_ids,
                "reason": str(
                    item.get(
                        "reason",
                        ""
                    )
                ),
            }
        )

    return {
        "prioritized_signals": validated,
        "signal_assessment": validated,
    }


# ============================================================
# NODE 10 — HUMAN REVIEW
# ============================================================

def human_review(
    state: ForecastState,
) -> ForecastState:

    review_payload = {
        "period": state["period"],
        "region": state["region"],
        "segment": state["segment"],
        "signals": state.get(
            "signal_assessment",
            []
        ),
        "hypotheses": state.get(
            "hypotheses",
            []
        ),
        "evidence": state.get(
            "evidence",
            []
        ),
    }

    decision = interrupt(
        review_payload
    )

    return {
        "human_review": decision
    }


# ============================================================
# NODE 11 — BUSINESS BRIEFING
# ============================================================

def generate_business_briefing(
    state: ForecastState,
) -> ForecastState:

    human_review_result = state.get(
        "human_review",
        {
            "status": "NOT_REQUIRED",
            "decision": "AUTO_EVALUATION",
            "comments": (
                "Human review disabled for evaluation."
            ),
        },
    )

    signal_assessment = state.get(
        "signal_assessment",
        []
    )

    prompt = f"""
You are a senior business intelligence analyst.

Generate an evidence-backed business briefing.

INVESTIGATION

Period: {state["period"]}
Region: {state["region"]}
Segment: {state["segment"]}

FORECAST MONITORING

{state.get("forecast_monitoring")}

DRIVER ANALYSIS

{state.get("driver_analysis")}

REVENUE TREND

{state.get("trend_analysis")}

EXTERNAL SIGNALS

{state.get("market_signals")}

SCENARIO ANALYSIS

{state.get("scenario_analysis")}

EVIDENCE

{state.get("evidence")}

SIGNAL ASSESSMENT

{signal_assessment}

HUMAN REVIEW

{human_review_result}

RULES

1. Distinguish facts, hypotheses, scenarios and recommendations.
2. Never claim causality from correlation.
3. Do not turn LOW signals into major drivers.
4. What-if analysis is a scenario estimate, not a forecast.
5. Recommendations must be tied to available evidence.
6. If no material investigation exists, explicitly state that
   no material forecast signal was detected.

Return ONLY valid JSON.

Format:

{{
  "executive_summary": "...",
  "recommendations": [
    {{
      "action": "...",
      "reason": "...",
      "priority": "HIGH"
    }}
  ],
  "briefing": "..."
}}
"""

    response = llm.invoke(
        prompt
    )

    raw = response.content.strip()

    try:
        parsed = json.loads(raw)

    except json.JSONDecodeError:

        parsed = {
            "executive_summary": raw,
            "recommendations": [],
            "briefing": raw,
        }

    recommendations = parsed.get(
        "recommendations",
        []
    )

    if not isinstance(
        recommendations,
        list
    ):
        recommendations = []

    return {
        "business_briefing": parsed.get(
            "briefing",
            parsed.get(
                "executive_summary",
                raw
            )
        ),
        "recommendations": recommendations,
        "human_review": human_review_result,
    }


# ============================================================
# ROUTING
# ============================================================

def route_after_forecast(
    state: ForecastState,
) -> str:

    monitoring = state.get(
        "forecast_monitoring",
        {}
    )

    if monitoring.get(
        "investigation_required",
        False
    ):
        return "investigate"

    return "briefing"


# ============================================================
# GRAPH
# ============================================================

def build_graph(
    include_human_review: bool = True,
):

    graph = StateGraph(
        ForecastState
    )

    graph.add_node(
        "initialize",
        initialize_investigation,
    )

    graph.add_node(
        "forecast",
        analyze_forecast,
    )

    graph.add_node(
        "analyze_drivers",
        analyze_drivers,
    )

    graph.add_node(
        "analyze_trends",
        analyze_trends,
    )

    graph.add_node(
        "analyze_market_signals",
        analyze_market_signals,
    )

    graph.add_node(
        "analyze_scenario",
        analyze_scenario,
    )

    graph.add_node(
        "consolidate_evidence",
        consolidate_evidence,
    )

    graph.add_node(
        "generate_hypotheses",
        generate_hypotheses,
    )

    graph.add_node(
        "prioritize_signals",
        prioritize_signals,
    )

    graph.add_node(
        "generate_business_briefing",
        generate_business_briefing,
    )

    if include_human_review:

        graph.add_node(
            "human_review",
            human_review,
        )

    graph.add_edge(
        START,
        "initialize",
    )

    graph.add_edge(
        "initialize",
        "forecast",
    )

    graph.add_conditional_edges(
        "forecast",
        route_after_forecast,
        {
            "investigate": "analyze_drivers",
            "briefing": "generate_business_briefing",
        },
    )

    graph.add_edge(
        "analyze_drivers",
        "analyze_trends",
    )

    graph.add_edge(
        "analyze_trends",
        "analyze_market_signals",
    )

    graph.add_edge(
        "analyze_market_signals",
        "analyze_scenario",
    )

    graph.add_edge(
        "analyze_scenario",
        "consolidate_evidence",
    )

    graph.add_edge(
        "consolidate_evidence",
        "generate_hypotheses",
    )

    graph.add_edge(
        "generate_hypotheses",
        "prioritize_signals",
    )

    if include_human_review:

        graph.add_edge(
            "prioritize_signals",
            "human_review",
        )

        graph.add_edge(
            "human_review",
            "generate_business_briefing",
        )

    else:

        graph.add_edge(
            "prioritize_signals",
            "generate_business_briefing",
        )

    graph.add_edge(
        "generate_business_briefing",
        END,
    )

    memory = MemorySaver()

    return graph.compile(
        checkpointer=memory
    )


# ============================================================
# PUBLIC RUNNER
# ============================================================

def run_forecast_investigation(
    period: str,
    region: str,
    segment: str,
    include_human_review: bool = True,
    thread_id: str | None = None,
):

    app = build_graph(
        include_human_review=include_human_review
    )

    if thread_id is None:

        thread_id = (
            f"{period}-{region}-{segment}"
        )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "period": period,
        "region": region,
        "segment": segment,
    }

    if include_human_review:

        result = app.invoke(
            initial_state,
            config=config,
        )

        if "__interrupt__" in result:

            print(
                "\n"
                "====================================================\n"
                " HUMAN REVIEW REQUIRED\n"
                "===================================================="
            )

            print(
                result["__interrupt__"]
            )

            decision = input(
                "\nEnter approval decision "
                "(APPROVED/REJECTED): "
            ).strip().upper()

            result = app.invoke(
                Command(
                    resume={
                        "status": "COMPLETED",
                        "decision": decision,
                        "comments": (
                            "Human reviewer decision."
                        ),
                    }
                ),
                config=config,
            )

    else:

        result = app.invoke(
            initial_state,
            config=config,
        )

    return result


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    result = run_forecast_investigation(
        period="2026-03-01",
        region="West",
        segment="Enterprise",
        include_human_review=True,
    )

    print(
        "\n"
        "====================================================\n"
        " FINAL BUSINESS BRIEFING\n"
        "====================================================\n"
    )

    print(
        result.get(
            "business_briefing",
            "No briefing generated.",
        )
    )