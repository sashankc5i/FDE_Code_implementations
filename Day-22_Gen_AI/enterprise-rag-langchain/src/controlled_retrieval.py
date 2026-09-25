from pathlib import Path
import sys
from collections import Counter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(SRC_DIR))


from baseline_retrieval import retrieve


DEFAULT_THRESHOLD = 0.50
DEFAULT_TOP_K = 3
DEFAULT_SOURCE_DOMINANCE = 0.66


def controlled_retrieve(
    query,
    top_k=DEFAULT_TOP_K,
    threshold=DEFAULT_THRESHOLD,
    source_dominance=DEFAULT_SOURCE_DOMINANCE,
):
    """
    Retrieve documents using:

    1. Absolute similarity threshold.
    2. Source concentration among the top results.

    Evidence is accepted when:
    - at least one result meets the absolute threshold, OR
    - one source dominates the retrieved results.
    """

    results = retrieve(query, top_k=top_k)

    if not results:
        return []

    # Rule 1: absolute similarity threshold
    threshold_results = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    if threshold_results:
        return threshold_results

    # Rule 2: source concentration
    sources = [
        result["source"]
        for result in results
        if result.get("source")
    ]

    if not sources:
        return []

    source_counts = Counter(sources)

    dominant_source, dominant_count = source_counts.most_common(1)[0]

    dominance_ratio = dominant_count / len(results)

    if dominance_ratio >= source_dominance:
        return [
            result
            for result in results
            if result["source"] == dominant_source
        ]

    return []


def has_sufficient_evidence(
    results,
    threshold=DEFAULT_THRESHOLD,
    source_dominance=DEFAULT_SOURCE_DOMINANCE,
):
    """
    Determine whether a retrieved result set contains
    sufficient evidence.
    """

    if not results:
        return False

    # Absolute similarity evidence
    if any(
        result["score"] >= threshold
        for result in results
    ):
        return True

    # Source concentration evidence
    sources = [
        result["source"]
        for result in results
        if result.get("source")
    ]

    if not sources:
        return False

    source_counts = Counter(sources)

    _, dominant_count = source_counts.most_common(1)[0]

    dominance_ratio = dominant_count / len(results)

    return dominance_ratio >= source_dominance


def diagnose_query(
    query,
    top_k=5,
    threshold=DEFAULT_THRESHOLD,
    source_dominance=DEFAULT_SOURCE_DOMINANCE,
):
    """
    Display raw retrieval results and the resulting
    retrieval-control decision.
    """

    results = retrieve(query, top_k=top_k)

    print("\n========== RETRIEVAL DIAGNOSTIC ==========")
    print(f"\nQuery: {query}")
    print(f"Threshold: {threshold}")
    print(f"Source dominance: {source_dominance}")
    print(f"Raw results requested: {top_k}")

    if not results:
        print("\nNo retrieval results.")
        return results

    sources = [
        result["source"]
        for result in results
        if result.get("source")
    ]

    source_counts = Counter(sources)

    dominant_source = None
    dominance_ratio = 0.0

    if source_counts:
        dominant_source, dominant_count = (
            source_counts.most_common(1)[0]
        )

        dominance_ratio = dominant_count / len(results)

    print(
        f"\nDominant source: "
        f"{dominant_source if dominant_source else 'None'}"
    )

    print(
        f"Dominance ratio: "
        f"{dominance_ratio:.2f}"
    )

    for index, result in enumerate(results, start=1):
        passes_threshold = result["score"] >= threshold

        print(f"\n--- Result {index} ---")
        print(f"Score     : {result['score']:.4f}")
        print(
            f"Threshold : "
            f"{'PASS' if passes_threshold else 'FILTERED'}"
        )
        print(f"Source    : {result['source']}")
        print("Text      :")
        print(result["text"][:1000])

    accepted = controlled_retrieve(
        query=query,
        top_k=min(top_k, DEFAULT_TOP_K),
        threshold=threshold,
        source_dominance=source_dominance,
    )

    print("\n========== CONTROL DECISION ==========")

    if accepted:
        print("Decision: ACCEPT")
        print("Accepted sources:")

        for result in accepted:
            print(
                f"- {result['source']} "
                f"(score={result['score']:.4f})"
            )
    else:
        print("Decision: ABSTAIN")

    return results


if __name__ == "__main__":
    query = "What should never be committed to source control?"

    diagnose_query(
        query=query,
        top_k=5,
        threshold=DEFAULT_THRESHOLD,
        source_dominance=DEFAULT_SOURCE_DOMINANCE,
    )