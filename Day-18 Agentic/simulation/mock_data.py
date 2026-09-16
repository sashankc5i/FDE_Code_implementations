PIPELINE_STATUS = {
    "customer_360": {
        "status": "FAILED",
        "last_error": (
            "AnalysisException: "
            "cannot resolve column 'customer_segment'"
        ),
    }
}


PIPELINE_LOGS = {
    "customer_360": [
        "Starting Customer 360 pipeline",
        "Bronze ingestion completed",
        "Silver transformation started",
        "AnalysisException: cannot resolve column 'customer_segment'",
        "Pipeline execution failed",
    ]
}


TABLE_SCHEMAS = {
    "customer_360": {
        "yesterday": {
            "customer_id": "INT",
            "customer_segment": "STRING",
            "customer_name": "STRING",
        },
        "today": {
            "customer_id": "INT",
            "segment": "STRING",
            "customer_name": "STRING",
        },
    }
}