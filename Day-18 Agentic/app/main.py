from app.agents.incident_agent import run_agent


def main() -> None:

    user_input = """
    The Customer 360 pipeline failed.

    Investigate the pipeline and tell me:
    1. What happened?
    2. What evidence do you have?
    3. What should we investigate next?
    """

    result = run_agent(user_input)

    print("\n=== INCIDENT AGENT ===\n")
    print(result)


if __name__ == "__main__":
    main()