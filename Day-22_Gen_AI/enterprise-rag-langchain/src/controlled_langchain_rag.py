from src.langchain_model import model
from src.langchain_prompt import prompt
from src.langchain_retriever import EngineeringRetriever


THRESHOLD = 0.50


def retrieve_with_control(question, top_k=3, threshold=THRESHOLD):
    """
    Retrieve documents and keep only results above the
    configured similarity threshold.
    """

    retriever = EngineeringRetriever()

    documents = retriever.invoke(question)

    controlled_documents = []

    for document in documents[:top_k]:
        score = document.metadata.get("score", 0.0)

        if score >= threshold:
            controlled_documents.append(document)

    return controlled_documents


def format_context(documents):
    """
    Convert retrieved LangChain Documents into the
    context format expected by the prompt.
    """

    if not documents:
        return ""

    context_parts = []

    for document in documents:
        source = document.metadata.get("source", "unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def answer_question(question):
    """
    Answer a question using controlled retrieval.

    If no sufficiently relevant evidence is found,
    abstain instead of sending unsupported context
    to the model.
    """

    documents = retrieve_with_control(question)

    if not documents:
        return {
            "answer": (
                "The available knowledge base is insufficient "
                "to answer this question."
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

    sources = []

    for document in documents:
        source = document.metadata.get("source")

        if source and source not in sources:
            sources.append(source)

    return {
        "answer": response.content,
        "sources": sources,
    }


if __name__ == "__main__":
    question = "What are common causes of HTTP 401 errors?"

    result = answer_question(question)

    print("\n========== CONTROLLED LANGCHAIN RAG ==========")
    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for source in result["sources"]:
        print(f"- {source}")