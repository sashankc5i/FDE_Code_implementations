import json
from pathlib import Path

from src.controlled_langchain_rag import answer_question


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EVALUATION_FILE = PROJECT_ROOT / "evaluation" / "questions.json"


def evaluate_question(item):
    """
    Evaluate one question against the expected source set.

    A question passes when at least one expected source
    is present in the retrieved source set.

    For out-of-domain questions, the expected source set
    is empty and the test passes only when no source
    is retrieved.
    """

    question = item["question"]
    expected_sources = set(item["expected_sources"])

    result = answer_question(question)

    actual_sources = set(result["sources"])

    if not expected_sources:
        success = len(actual_sources) == 0
    else:
        success = bool(
            expected_sources.intersection(actual_sources)
        )

    matched_sources = expected_sources.intersection(
        actual_sources
    )

    return {
        "question": question,
        "expected_sources": expected_sources,
        "actual_sources": actual_sources,
        "matched_sources": matched_sources,
        "success": success,
    }


def main():
    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8",
    ) as file:
        questions = json.load(file)

    passed = 0

    print("\n========== CONTROLLED RAG EVALUATION ==========")

    for index, item in enumerate(questions, start=1):
        result = evaluate_question(item)

        if result["success"]:
            passed += 1

        print(f"\nQuestion {index}:")
        print(result["question"])

        print(
            f"Expected sources: "
            f"{sorted(result['expected_sources'])}"
        )

        print(
            f"Retrieved sources: "
            f"{sorted(result['actual_sources'])}"
        )

        print(
            f"Matched sources: "
            f"{sorted(result['matched_sources'])}"
        )

        print(
            f"Result: "
            f"{'PASS' if result['success'] else 'FAIL'}"
        )

    total = len(questions)

    score = (
        (passed / total) * 100
        if total > 0
        else 0
    )

    print("\n========== SUMMARY ==========")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    print(f"Score: {score:.2f}%")


if __name__ == "__main__":
    main()