from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import os


load_dotenv()


# --------------------------------------------------
# Model
# --------------------------------------------------

model = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)


# --------------------------------------------------
# Tool 1: Engineering Knowledge
# --------------------------------------------------

@tool
def search_engineering_knowledge(query: str) -> str:
    """
    Search the engineering knowledge base for
    engineering and troubleshooting information.
    """

    knowledge_base = {
        "401": """
HTTP 401 errors can occur because of expired tokens,
invalid tokens, incorrect token audiences, or incorrect
authentication configuration.
""",
        "custom domain": """
After introducing a custom domain to Azure Container Apps,
validate DNS configuration, TLS certificate configuration,
redirect URIs, authentication configuration, and token audience.
""",
        "database": """
For a slow database query, investigate execution plans,
indexes, blocking, waits, statistics, data volume,
and potentially expensive joins.
""",
    }

    query_lower = query.lower()

    results = []

    for keyword, information in knowledge_base.items():
        if keyword in query_lower:
            results.append(information.strip())

    if not results:
        return (
            "No relevant information was found in the "
            "engineering knowledge base."
        )

    return "\n\n".join(results)


# --------------------------------------------------
# Tool 2: Calculator
# --------------------------------------------------

@tool
def calculate(expression: str) -> str:
    """
    Calculate a basic mathematical expression.
    """

    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)

    except Exception:
        return "Unable to calculate the expression."


# --------------------------------------------------
# Agent
# --------------------------------------------------

agent = create_agent(
    model=model,
    tools=[
        search_engineering_knowledge,
        calculate,
    ],
    system_prompt="""
You are an enterprise engineering assistant.

Use the engineering knowledge tool when the user
asks about engineering documentation or troubleshooting.

Use the calculator when mathematical computation
is required.

Do not invent engineering information.

If the available tools do not provide sufficient
evidence, clearly state that you do not have enough
information.
""",
)


# --------------------------------------------------
# Test
# --------------------------------------------------

if __name__ == "__main__":

    question = (
        "What are common causes of HTTP 401 errors?"
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        }
    )

    print("\n========== LANGCHAIN AGENT ==========")

    for message in result["messages"]:
        print(f"\n{message.type}:")
        print(message.content)