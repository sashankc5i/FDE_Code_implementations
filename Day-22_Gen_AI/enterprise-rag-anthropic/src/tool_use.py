def search_engineering_knowledge(query: str) -> str:
    knowledge_base = {
        "401": (
            "Common HTTP 401 causes include expired tokens, "
            "invalid tokens, incorrect token audience, "
            "missing authentication configuration, "
            "and incorrect client configuration."
        ),
        "custom domain": (
            "After introducing a custom domain to Azure Container Apps, "
            "validate DNS, domain binding, TLS, ingress configuration, "
            "redirect URIs, token audience, environment variables, "
            "and frontend-backend connectivity."
        ),
        "database": (
            "For a slow database query, inspect the execution plan, "
            "indexes, joins, filters, statistics, data volume, "
            "and query duration."
        )
    }

    query_lower = query.lower()

    for keyword, information in knowledge_base.items():
        if keyword in query_lower:
            return information

    return "No relevant engineering information was found."

def simulate_tool_call():
    tool_request = {
        "type": "tool_use",
        "name": "search_engineering_knowledge",
        "input": {
            "query": "HTTP 401 errors"
        }
    }

    print("\n========== TOOL REQUEST ==========")
    print(f"Tool: {tool_request['name']}")
    print(f"Input: {tool_request['input']}")

    result = search_engineering_knowledge(
        tool_request["input"]["query"]
    )

    tool_result = {
        "type": "tool_result",
        "tool_name": tool_request["name"],
        "content": result
    }

    print("\n========== TOOL RESULT ==========")
    print(f"Tool: {tool_result['tool_name']}")
    print(f"Content: {tool_result['content']}")


if __name__ == "__main__":
    simulate_tool_call()
if __name__ == "__main__":
    result = search_engineering_knowledge(
        "What causes HTTP 401 errors?"
    )

    print("\n========== TOOL EXECUTION ==========")
    print(result)

    