from langchain_core.prompts import ChatPromptTemplate

from langchain_model import model


# -----------------------------------------
# 1. Create reusable prompt template
# -----------------------------------------

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
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{question}
"""
        )
    ]
)


# -----------------------------------------
# 2. Provide input variables
# -----------------------------------------

context = """
HTTP 401 Unauthorized commonly occurs when
an access token is expired or invalid,
the token audience is incorrect, or
authentication configuration is incorrect.
"""

question = (
    "What are common causes of HTTP 401 errors?"
)


# -----------------------------------------
# 3. Render the prompt
# -----------------------------------------

messages = prompt.invoke(
    {
        "context": context,
        "question": question
    }
)


# -----------------------------------------
# 4. Inspect the generated messages
# -----------------------------------------

print(
    "\n========== PROMPT TEMPLATE =========="
)

for message in messages.messages:

    print(
        f"\n[{message.type.upper()}]"
    )

    print(
        message.content
    )


# -----------------------------------------
# 5. Send prompt to model
# -----------------------------------------

response = model.invoke(
    messages
)


print(
    "\n========== MODEL RESPONSE =========="
)

print(
    response.content
)