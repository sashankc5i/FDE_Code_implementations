import json
import sys
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

# Allow imports from both the project root and src/
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_DIR))


# --------------------------------------------------
# Application import
# --------------------------------------------------

from controlled_langchain_rag import answer_question


# --------------------------------------------------
# Evaluation data
# --------------------------------------------------

EVALUATION_FILE = (
    PROJECT_ROOT / "evaluation" / "questions.json"
)


# --------------------------------------------------
# Evaluation
# --------------------------------------------------

def main():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(file)


    passed = 0


    print("\n========== CONTROLLED RAG EVALUATION ==========")


    for index, item in enumerate(questions, start=1):

        question = item["question"]

        expected_sources = set(
            item["expected_sources"]
        )


        # Run the RAG application
        result = answer_question(question)


        actual_sources = set(
            result["sources"]
        )


        # --------------------------------------------------
        # Evaluation logic
        # --------------------------------------------------

        if not expected_sources:

            # For out-of-domain questions,
            # we expect the system to abstain.
            success = len(actual_sources) == 0

        else:

            # At least one expected source should
            # be retrieved.
            success = bool(
                expected_sources.intersection(
                    actual_sources
                )
            )


        if success:
            passed += 1


        # --------------------------------------------------
        # Print result
        # --------------------------------------------------

        print(f"\nQuestion {index}:")
        print(question)

        print(
            f"Expected sources: "
            f"{sorted(expected_sources)}"
        )

        print(
            f"Retrieved sources: "
            f"{sorted(actual_sources)}"
        )

        print(
            f"Result: "
            f"{'PASS' if success else 'FAIL'}"
        )


    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    total = len(questions)

    score = (
        (passed / total) * 100
        if total > 0
        else 0
    )


    print("\n========== SUMMARY ==========")

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Score: {score:.2f}%"
    )


# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()