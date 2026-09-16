from app.agents.supervisor import run_parallel_investigation


def test_supervisor():

    result = run_parallel_investigation(
        pipeline_id="customer_360",
        table_name="customer_master",
        incident_description=(
            "Customer 360 pipeline failed with "
            "AnalysisException: Cannot resolve column "
            "'customer_segment'. Logs show the failure "
            "occurred during the silver transformation."
        ),
    )

    print("\n=== SUPERVISOR DECISION ===")
    print(result["decision"])

    print("\n=== SPECIALIST RESULTS ===")

    for investigation in result["investigations"]:
        print(
            investigation["agent"],
            "->",
            investigation["status"],
        )

    assert result["status"] == "COMPLETED"

    assert "log" in result["decision"]["investigations"]

    assert "data" in result["decision"]["investigations"]