from langchain_core.tools import tool


@tool
def search_engineering_knowledge(query: str) -> str:
    """
    Search the engineering knowledge base for information
    related to the user's query.
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


if __name__ == "__main__":

    result = search_engineering_knowledge.invoke(
        "What are common causes of HTTP 401 errors?"
    )

    print("\n========== LANGCHAIN TOOL ==========")
    print(result)