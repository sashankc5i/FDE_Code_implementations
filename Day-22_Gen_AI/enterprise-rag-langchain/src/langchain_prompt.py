from langchain_core.prompts import ChatPromptTemplate

from src.langchain_model import model


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an enterprise engineering knowledge assistant.

Answer the user's question clearly and concisely.

If the provided context does not contain
enough information to answer the question,
say that the available knowledge base
is insufficient.
""",
        ),
        (
            "human",
            """
Context:

{context}

Question:
{question}
""",
        ),
    ]
)


if __name__ == "__main__":
    test_input = {
        "context": """
HTTP 401 Unauthorized commonly occurs when
an access token is expired or invalid,
the token audience is incorrect, or
authentication configuration is incorrect.
""",
        "question": "What are common causes of HTTP 401 errors?",
    }

    formatted_prompt = prompt.invoke(test_input)

    print("\n========== PROMPT TEMPLATE ==========")
    print(formatted_prompt)

    response = model.invoke(formatted_prompt)

    print("\n========== MODEL RESPONSE ==========")
    print(response.content)