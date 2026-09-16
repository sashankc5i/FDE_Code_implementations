GROUND_TRUTH = {
    "INC-001": {
        "failure_type": "SCHEMA_DRIFT",
        "expected_pipeline": "customer_360",
        "expected_root_cause": (
            "customer_segment is referenced by the "
            "transformation but the source schema contains segment"
        ),
    },

    "INC-2026-0916-001": {
        "failure_type": "SCHEMA_DRIFT",
        "expected_pipeline": "customer_360",
        "expected_root_cause": (
            "customer_segment is referenced by the "
            "transformation but the source schema contains segment"
        ),
    },
}