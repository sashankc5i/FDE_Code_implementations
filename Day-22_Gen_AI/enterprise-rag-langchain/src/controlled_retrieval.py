from baseline_retrieval import retrieve


DEFAULT_THRESHOLD = 0.50


def controlled_retrieve(
    query: str,
    top_k: int = 3,
    threshold: float = DEFAULT_THRESHOLD,
):
    """
    Retrieve documents and reject results whose
    similarity score is below the configured threshold.
    """

    results = retrieve(query, top_k=top_k)

    accepted = [
        result
        for result in results
        if result["score"] >= threshold
    ]

    return accepted


def has_sufficient_evidence(
    results,
    minimum_results: int = 1,
):
    """
    Determine whether enough relevant evidence exists
    to answer the question.
    """

    return len(results) >= minimum_results


if __name__ == "__main__":

    test_questions = [
        "What are common causes of HTTP 401 errors?",
        "How do I configure Kubernetes horizontal pod autoscaling?",
    ]

    for question in test_questions:

        print("\n================================")
        print(f"Question: {question}")

        results = controlled_retrieve(
            question,
            top_k=3,
            threshold=DEFAULT_THRESHOLD,
        )

        if not has_sufficient_evidence(results):

            print("ABSTAIN")
            print(
                "I don't have sufficient evidence "
                "in the engineering knowledge base "
                "to answer this."
            )
            continue

        print("EVIDENCE FOUND")

        for result in results:
            print(
                f"\nSource: {result['source']}"
                f"\nScore: {result['score']:.4f}"
            )