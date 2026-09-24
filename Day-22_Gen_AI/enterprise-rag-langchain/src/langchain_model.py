import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# -----------------------------------------
# 1. Load environment variables
# -----------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Add it to your .env file."
    )


# -----------------------------------------
# 2. Create LangChain model
# -----------------------------------------

model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY
)


# -----------------------------------------
# 3. Test model invocation
# -----------------------------------------

if __name__ == "__main__":

    response = model.invoke(
        "Explain what an HTTP 401 error means "
        "in one sentence."
    )

    print(
        "\n========== LANGCHAIN MODEL =========="
    )

    print(
        response.content
    )