from unittest.mock import patch

from app.agents.supervisor import run_parallel_investigation


def test_specialist_failure_isolated():

    with patch(
        "app.agents.supervisor.investigate_logs",
        side_effect=Exception(
            "Simulated log system failure"
        ),
    ):

        result = run_parallel_investigation(
            pipeline_id="customer_360",
            table_name="customer_master",
            incident_description=(
                "Customer 360 pipeline failed with "
                "AnalysisException: Cannot resolve column "
                "'customer_segment'."
            ),
        )

    print("\n=== FAILURE ISOLATION TEST ===")

    for investigation in result["investigations"]:

        print(
            investigation["agent"],
            "->",
            investigation["status"],
        )

        if investigation["status"] == "FAILED":
            print(
                "Error:",
                investigation["error"],
            )

    assert result["status"] == "COMPLETED"

    log_result = next(
        item
        for item in result["investigations"]
        if item["agent"] == "log_agent"
    )

    data_result = next(
        item
        for item in result["investigations"]
        if item["agent"] == "data_agent"
    )

    assert log_result["status"] == "FAILED"

    assert data_result["status"] == "COMPLETED"