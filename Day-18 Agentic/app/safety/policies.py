READ = "READ"
LOW_RISK_WRITE = "LOW_RISK_WRITE"
HIGH_RISK_WRITE = "HIGH_RISK_WRITE"
DESTRUCTIVE = "DESTRUCTIVE"


TOOL_RISK = {
    "get_pipeline_status": READ,
    "get_pipeline_logs": READ,
    "get_table_schema": READ,
    "find_pipeline": READ,

    "create_incident": LOW_RISK_WRITE,

    "restart_pipeline": HIGH_RISK_WRITE,
    "rollback_deployment": HIGH_RISK_WRITE,

    "disable_pipeline": DESTRUCTIVE,
}