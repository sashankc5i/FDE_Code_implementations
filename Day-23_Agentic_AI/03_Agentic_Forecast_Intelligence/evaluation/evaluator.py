import json
from pathlib import Path
from typing import Any


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_FILE = (
    BASE_DIR
    / "evaluation"
    / "dataset.json"
)


# ============================================================
# DATASET
# ============================================================

def load_dataset() -> list[dict[str, Any]]:
    """
    Load evaluation cases from dataset.json.

    Expected structure:

    {
        "evaluation_cases": [
            {...},
            {...}
        ]
    }
    """

    with open(
        DATASET_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(
        data,
        dict,
    ):
        raise ValueError(
            "Evaluation dataset must be a JSON object."
        )

    cases = data.get(
        "evaluation_cases",
        [],
    )

    if not isinstance(
        cases,
        list,
    ):
        raise ValueError(
            "'evaluation_cases' must be a list."
        )

    return cases


# ============================================================
# SIGNAL NORMALIZATION
# ============================================================

SIGNAL_ALIASES = {
    "pipeline": "pipeline_deterioration",
    "pipeline_deterioration": "pipeline_deterioration",

    "revenue": "revenue_deterioration",
    "revenue_deterioration": "revenue_deterioration",

    "churn": "customer_churn",
    "customer_churn": "customer_churn",

    "external_demand": "external_demand",
    "demand": "external_demand",

    "pricing": "pricing",
}


def normalize_signal(
    signal: str,
) -> str | None:

    if not signal:
        return None

    return SIGNAL_ALIASES.get(
        signal.strip().lower()
    )


# ============================================================
# STRUCTURED SIGNAL EXTRACTION
# ============================================================

def extract_signal_details(
    agent_result: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Extract structured signal assessments from the agent.
    """

    assessment = agent_result.get(
        "signal_assessment",
        [],
    )

    if not isinstance(
        assessment,
        list,
    ):
        return []

    return [
        item
        for item in assessment
        if isinstance(
            item,
            dict,
        )
    ]


def extract_predicted_signals(
    agent_result: dict[str, Any],
) -> list[str]:
    """
    Only HIGH and MEDIUM detected signals are considered
    material business signals.
    """

    signal_details = extract_signal_details(
        agent_result
    )

    predicted = []

    for item in signal_details:

        signal = normalize_signal(
            item.get(
                "signal",
                "",
            )
        )

        detected = bool(
            item.get(
                "detected",
                False,
            )
        )

        priority = str(
            item.get(
                "priority",
                "LOW",
            )
        ).upper()

        if (
            signal
            and detected
            and priority in {
                "HIGH",
                "MEDIUM",
            }
        ):

            predicted.append(
                signal
            )

    return list(
        dict.fromkeys(
            predicted
        )
    )


# ============================================================
# PRIORITY EXTRACTION
# ============================================================

def extract_predicted_priority(
    agent_result: dict[str, Any],
) -> dict[str, str]:
    """
    Return:

        {
            "pipeline_deterioration": "HIGH",
            "external_demand": "MEDIUM"
        }
    """

    details = extract_signal_details(
        agent_result
    )

    priorities = {}

    for item in details:

        signal = normalize_signal(
            item.get(
                "signal",
                "",
            )
        )

        if not signal:
            continue

        if not item.get(
            "detected",
            False,
        ):
            continue

        priorities[signal] = str(
            item.get(
                "priority",
                "LOW",
            )
        ).upper()

    return priorities


# ============================================================
# PRECISION
# ============================================================

def calculate_precision(
    predicted: list[str],
    expected: list[str],
) -> float:

    predicted_set = set(
        predicted
    )

    expected_set = set(
        expected
    )

    if not predicted_set:

        return (
            1.0
            if not expected_set
            else 0.0
        )

    true_positive = len(
        predicted_set
        & expected_set
    )

    return round(
        true_positive
        / len(predicted_set),
        3,
    )


# ============================================================
# RECALL
# ============================================================

def calculate_recall(
    predicted: list[str],
    expected: list[str],
) -> float:

    predicted_set = set(
        predicted
    )

    expected_set = set(
        expected
    )

    if not expected_set:

        return (
            1.0
            if not predicted_set
            else 0.0
        )

    true_positive = len(
        predicted_set
        & expected_set
    )

    return round(
        true_positive
        / len(expected_set),
        3,
    )


# ============================================================
# FALSE POSITIVES
# ============================================================

def calculate_false_positives(
    predicted: list[str],
    expected: list[str],
) -> list[str]:

    return sorted(
        set(predicted)
        - set(expected)
    )


# ============================================================
# FALSE NEGATIVES
# ============================================================

def calculate_false_negatives(
    predicted: list[str],
    expected: list[str],
) -> list[str]:

    return sorted(
        set(expected)
        - set(predicted)
    )


# ============================================================
# RELEVANCE
# ============================================================

def calculate_relevance(
    predicted: list[str],
    expected: list[str],
) -> float:

    return calculate_precision(
        predicted,
        expected,
    )


# ============================================================
# PRIORITY ACCURACY
# ============================================================

def calculate_priority_accuracy(
    case: dict[str, Any],
    agent_result: dict[str, Any],
) -> float:
    """
    Evaluate whether the agent assigned appropriate
    HIGH / MEDIUM / LOW priorities.

    Expected priority comes from the evaluation dataset.
    """

    predicted = extract_predicted_priority(
        agent_result
    )

    expected_high = {
        normalize_signal(signal)
        for signal in case.get(
            "high_priority_signals",
            [],
        )
    }

    expected_medium = {
        normalize_signal(signal)
        for signal in case.get(
            "medium_priority_signals",
            [],
        )
    }

    expected_low = {
        normalize_signal(signal)
        for signal in case.get(
            "low_priority_signals",
            [],
        )
    }

    expected_priority = {}

    for signal in expected_high:
        if signal:
            expected_priority[signal] = "HIGH"

    for signal in expected_medium:
        if signal:
            expected_priority[signal] = "MEDIUM"

    for signal in expected_low:
        if signal:
            expected_priority[signal] = "LOW"

    if not expected_priority and not predicted:
        return 1.0

    all_signals = (
        set(expected_priority)
        | set(predicted)
    )

    if not all_signals:
        return 1.0

    correct = 0

    for signal in all_signals:

        expected_priority_value = (
            expected_priority.get(
                signal,
                "NONE",
            )
        )

        predicted_priority_value = (
            predicted.get(
                signal,
                "NONE",
            )
        )

        if (
            expected_priority_value
            == predicted_priority_value
        ):
            correct += 1

    return round(
        correct
        / len(all_signals),
        3,
    )


# ============================================================
# EVIDENCE QUALITY
# ============================================================

def calculate_evidence_quality(
    signal_details: list[dict[str, Any]],
) -> float:

    material_signals = [
        item
        for item in signal_details
        if item.get(
            "detected",
            False,
        )
        and str(
            item.get(
                "priority",
                "",
            )
        ).upper()
        in {
            "HIGH",
            "MEDIUM",
        }
    ]

    if not material_signals:
        return 1.0

    supported = 0

    for item in material_signals:

        evidence_ids = item.get(
            "evidence_ids",
            [],
        )

        if (
            isinstance(
                evidence_ids,
                list,
            )
            and evidence_ids
        ):

            supported += 1

    return round(
        supported
        / len(material_signals),
        3,
    )


# ============================================================
# GROUNDEDNESS
# ============================================================

def calculate_groundedness(
    signal_details: list[dict[str, Any]],
    available_evidence_ids: list[str],
) -> float:

    material_signals = [
        item
        for item in signal_details
        if item.get(
            "detected",
            False,
        )
        and str(
            item.get(
                "priority",
                "",
            )
        ).upper()
        in {
            "HIGH",
            "MEDIUM",
        }
    ]

    if not material_signals:
        return 1.0

    available = set(
        available_evidence_ids
    )

    grounded = 0

    for item in material_signals:

        evidence_ids = item.get(
            "evidence_ids",
            [],
        )

        if not evidence_ids:
            continue

        if all(
            evidence_id in available
            for evidence_id in evidence_ids
        ):

            grounded += 1

    return round(
        grounded
        / len(material_signals),
        3,
    )


# ============================================================
# ACTIONABILITY
# ============================================================

def calculate_actionability(
    agent_result: dict[str, Any],
) -> float:

    recommendations = agent_result.get(
        "recommendations",
        [],
    )

    if not recommendations:
        return 0.0

    if not isinstance(
        recommendations,
        list,
    ):
        return 0.0

    valid = 0

    for recommendation in recommendations:

        if isinstance(
            recommendation,
            str,
        ):

            if recommendation.strip():
                valid += 1

        elif isinstance(
            recommendation,
            dict,
        ):

            if recommendation.get(
                "action"
            ):

                valid += 1

    return round(
        valid
        / len(recommendations),
        3,
    )


# ============================================================
# HUMAN ACCEPTANCE
# ============================================================

def calculate_human_acceptance(
    agent_result: dict[str, Any],
) -> float | None:

    human_review = agent_result.get(
        "human_review"
    )

    if not human_review:
        return None

    decision = str(
        human_review.get(
            "decision",
            "",
        )
    ).upper()

    if decision in {
        "APPROVED",
        "ACCEPTED",
        "YES",
    }:

        return 1.0

    if decision in {
        "REJECTED",
        "DECLINED",
        "NO",
    }:

        return 0.0

    return None


# ============================================================
# CASE EVALUATION
# ============================================================

def evaluate_case(
    case: dict[str, Any],
    agent_result: dict[str, Any],
) -> dict[str, Any]:

    expected = [
        normalize_signal(
            signal
        )
        for signal in case.get(
            "ground_truth_signals",
            [],
        )
    ]

    expected = [
        signal
        for signal in expected
        if signal
    ]

    predicted = extract_predicted_signals(
        agent_result
    )

    signal_details = extract_signal_details(
        agent_result
    )

    available_evidence = [
        item.get(
            "evidence_id"
        )
        for item in agent_result.get(
            "evidence",
            []
        )
        if isinstance(
            item,
            dict,
        )
        and item.get(
            "evidence_id"
        )
    ]

    return {
        "case_id": case["case_id"],

        "predicted_signals": predicted,

        "expected_signals": expected,

        "predicted_priority":
            extract_predicted_priority(
                agent_result
            ),

        "precision":
            calculate_precision(
                predicted,
                expected,
            ),

        "recall":
            calculate_recall(
                predicted,
                expected,
            ),

        "relevance":
            calculate_relevance(
                predicted,
                expected,
            ),

        "priority_accuracy":
            calculate_priority_accuracy(
                case,
                agent_result,
            ),

        "false_positives":
            calculate_false_positives(
                predicted,
                expected,
            ),

        "false_negatives":
            calculate_false_negatives(
                predicted,
                expected,
            ),

        "evidence_quality":
            calculate_evidence_quality(
                signal_details
            ),

        "groundedness":
            calculate_groundedness(
                signal_details,
                available_evidence,
            ),

        "actionability":
            calculate_actionability(
                agent_result
            ),

        "human_acceptance":
            calculate_human_acceptance(
                agent_result
            ),
    }


# ============================================================
# AGGREGATION
# ============================================================

def aggregate_results(
    results: list[dict[str, Any]],
) -> dict[str, Any]:

    if not results:
        return {
            "cases_evaluated": 0
        }

    def average(
        field: str,
    ) -> float:

        values = [
            result[field]
            for result in results
            if result[field] is not None
        ]

        if not values:
            return 0.0

        return round(
            sum(values)
            / len(values),
            3,
        )

    return {
        "cases_evaluated":
            len(results),

        "average_precision":
            average(
                "precision"
            ),

        "average_recall":
            average(
                "recall"
            ),

        "average_relevance":
            average(
                "relevance"
            ),

        "average_priority_accuracy":
            average(
                "priority_accuracy"
            ),

        "average_evidence_quality":
            average(
                "evidence_quality"
            ),

        "average_groundedness":
            average(
                "groundedness"
            ),

        "average_actionability":
            average(
                "actionability"
            ),

        "human_acceptance_rate":
            average(
                "human_acceptance"
            ),

        "total_false_positives":
            sum(
                len(
                    result[
                        "false_positives"
                    ]
                )
                for result in results
            ),

        "total_false_negatives":
            sum(
                len(
                    result[
                        "false_negatives"
                    ]
                )
                for result in results
            ),
    }