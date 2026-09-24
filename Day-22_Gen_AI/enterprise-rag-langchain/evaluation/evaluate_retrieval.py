import json
import sys
from pathlib import Path


# -----------------------------------------
# Add project root to Python path
# -----------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from src.baseline_retrieval import retrieve


# -----------------------------------------
# Paths
# -----------------------------------------

QUESTIONS_PATH = Path(
    "evaluation/questions.json"
)


# -----------------------------------------
# Load evaluation questions
# -----------------------------------------

with open(
    QUESTIONS_PATH,
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


# -----------------------------------------
# Evaluate retrieval
# -----------------------------------------

print(
    "\n========== RETRIEVAL EVALUATION =========="
)


total = len(questions)
passed = 0


for number, item in enumerate(
    questions,
    start=1
):

    question = item["question"]

    expected_sources = set(
        item["expected_sources"]
    )

    results = retrieve(
        question,
        top_k=3
    )

    retrieved_sources = {
        result["source"]
        for result in results
    }

    if expected_sources:

        matched_sources = (
            expected_sources
            & retrieved_sources
        )

        success = bool(
            matched_sources
        )

    else:

        # Out-of-domain questions should
        # not retrieve a known source as
        # a strong answer source.
        success = (
            len(retrieved_sources) == 0
        )

    if success:
        passed += 1

    print(
        f"\nQuestion {number}:"
    )

    print(
        question
    )

    print(
        f"Expected: "
        f"{sorted(expected_sources)}"
    )

    print(
        f"Retrieved: "
        f"{sorted(retrieved_sources)}"
    )

    print(
        f"Result: "
        f"{'PASS' if success else 'FAIL'}"
    )


# -----------------------------------------
# Summary
# -----------------------------------------

accuracy = (
    passed / total * 100
    if total
    else 0
)

print(
    "\n========== SUMMARY =========="
)

print(
    f"Passed: {passed}/{total}"
)

print(
    f"Retrieval coverage: {accuracy:.2f}%"
)