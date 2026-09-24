from langchain_model import model
from langchain_prompt import prompt
from langchain_retriever import EngineeringRetriever


THRESHOLD = 0.50


def retrieve_with_control(question: str):
    retriever = EngineeringRetriever(k=3)

    documents = retriever.invoke(question)

    accepted_documents = [
        document
        for document in documents
        if document.metadata["score"] >= THRESHOLD
    ]

    return accepted_documents


def format_context(documents):

    context_parts = []

    for document in documents:

        source = document.metadata["source"]

        context_parts.append(
            f"[Source: {source}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def answer_question(question: str):

    documents = retrieve_with_control(question)

    if not documents:

        return {
            "answer": (
                "I don't have sufficient evidence in the "
                "engineering knowledge base to answer this."
            ),
            "sources": [],
        }

    context = format_context(documents)

    response = (
        prompt
        | model
    ).invoke(
        {
            "context": context,
            "question": question,
        }
    )

    sources = list(
        dict.fromkeys(
            document.metadata["source"]
            for document in documents
        )
    )

    return {
        "answer": response.content,
        "sources": sources,
    }


if __name__ == "__main__":

    questions = [
        "What are common causes of HTTP 401 errors?",
        "How do I configure Kubernetes horizontal pod autoscaling?",
    ]

    for question in questions:

        print("\n======================================")
        print(f"QUESTION: {question}")

        result = answer_question(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")
        if result["sources"]:
            for source in result["sources"]:
                print(f"- {source}")
        else:
            print("- None")