from langchain_model import model
from langchain_prompt import prompt
from langchain_retriever import EngineeringRetriever


def format_documents(documents):
    """
    Convert LangChain Documents into a context string.
    """

    context_parts = []

    for document in documents:

        source = document.metadata["source"]

        context_parts.append(
            f"[Source: {source}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def build_rag_chain():

    retriever = EngineeringRetriever(k=3)

    def retrieve_and_format(inputs):

        documents = retriever.invoke(
            inputs["question"]
        )

        context = format_documents(documents)

        return {
            "context": context,
            "question": inputs["question"],
        }

    chain = (
        retrieve_and_format
        | prompt
        | model
    )

    return chain


if __name__ == "__main__":

    chain = build_rag_chain()

    question = (
        "What should I check after introducing "
        "a custom domain to an Azure Container App?"
    )

    response = chain.invoke({
        "question": question
    })

    print("\n========== LANGCHAIN RAG ==========")
    print(response.content)