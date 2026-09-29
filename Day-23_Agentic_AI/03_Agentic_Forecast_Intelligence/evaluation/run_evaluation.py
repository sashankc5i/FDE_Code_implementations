from pathlib import Path
import sys


# ============================================================
# PATH
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)

if str(BASE_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(BASE_DIR),
    )


# ============================================================
# IMPORTS
# ============================================================

from src.forecast_agent import (
    run_forecast_investigation,
)

from evaluation.evaluator import (
    load_dataset,
    evaluate_case,
    aggregate_results,
)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "\n"
        "====================================================\n"
        " AGENT SIGNAL EVALUATION\n"
        "===================================================="
    )

    dataset = load_dataset()

    print(
        f"\nEvaluation cases loaded: "
        f"{len(dataset)}"
    )

    results = []

    for case in dataset:

        print(
            f"\nRunning "
            f"{case['case_id']}..."
        )

        agent_result = (
            run_forecast_investigation(
                period=case["period"],
                region=case["region"],
                segment=case["segment"],
                include_human_review=False,
            )
        )

        result = evaluate_case(
            case,
            agent_result,
        )

        results.append(
            result
        )

        print(
            f"Predicted : "
            f"{result['predicted_signals']}"
        )

        print(
            f"Expected  : "
            f"{result['expected_signals']}"
        )

        print(
            f"Priority  : "
            f"{result['predicted_priority']}"
        )

        print(
            f"Precision : "
            f"{result['precision']}"
        )

        print(
            f"Recall    : "
            f"{result['recall']}"
        )

        print(
            f"Relevance : "
            f"{result['relevance']}"
        )

        print(
            f"Priority Accuracy : "
            f"{result['priority_accuracy']}"
        )

        print(
            f"Evidence  : "
            f"{result['evidence_quality']}"
        )

        print(
            f"Grounded  : "
            f"{result['groundedness']}"
        )

        print(
            f"Actionable: "
            f"{result['actionability']}"
        )

        print(
            f"FP        : "
            f"{result['false_positives']}"
        )

        print(
            f"FN        : "
            f"{result['false_negatives']}"
        )

    aggregate = aggregate_results(
        results
    )

    print(
        "\n"
        "====================================================\n"
        " AGGREGATE RESULTS\n"
        "===================================================="
    )

    for key, value in aggregate.items():

        print(
            f"{key}: {value}"
        )