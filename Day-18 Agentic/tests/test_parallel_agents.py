from app.agents.supervisor import run_parallel_investigation


def test_parallel_investigation():

    result = run_parallel_investigation(
        pipeline_id="customer_360",
        table_name="customer_master",
    )

    print("\n=== PARALLEL INVESTIGATION ===")

    for investigation in result["investigations"]:
        print(
            f"\nAgent: {investigation['agent']}"
        )

        print(
            f"Status: {investigation['status']}"
        )

        print(
            f"Findings: {investigation['findings']}"
        )

    assert result["status"] == "COMPLETED"