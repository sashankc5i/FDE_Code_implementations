from langchain_model import model
from langchain_prompt import prompt


def get_context(question: str) -> str:
    """
    Temporary context provider.

    In the real RAG application, this function
    will be replaced by our vector database retriever.
    """

    return """
    HTTP 401 errors can occur because of:
    - expired access tokens
    - invalid tokens
    - incorrect token audience
    - incorrect authentication configuration

    When troubleshooting a 401 error, validate the
    token, audience, issuer, and authentication settings.
    """


def build_chain():
    """
    Build the application chain.
    """

    chain = (
        {
            "context": lambda inputs: get_context(inputs["question"]),
            "question": lambda inputs: inputs["question"],
        }
        | prompt
        | model
    )

    return chain


if __name__ == "__main__":

    chain = build_chain()

    question = "What are common causes of HTTP 401 errors?"

    response = chain.invoke({
        "question": question
    })

    print("\n========== LANGCHAIN CHAIN ==========")
    print(response.content)