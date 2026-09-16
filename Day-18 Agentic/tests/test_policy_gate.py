from app.safety.policy_gate import evaluate_action


def test_read_action_allowed():

    result = evaluate_action(
        "get_pipeline_logs"
    )

    assert result["allowed"] is True
    assert result["requires_human"] is False


def test_restart_requires_approval():

    result = evaluate_action(
        "restart_pipeline"
    )

    assert result["allowed"] is False
    assert result["requires_human"] is True


def test_rollback_requires_approval():

    result = evaluate_action(
        "rollback_deployment"
    )

    assert result["allowed"] is False
    assert result["requires_human"] is True


def test_destructive_action_blocked():

    result = evaluate_action(
        "disable_pipeline"
    )

    assert result["allowed"] is False
    assert result["requires_human"] is True


def test_unknown_tool_blocked():

    result = evaluate_action(
        "delete_database"
    )

    assert result["allowed"] is False
    assert result["requires_human"] is True