FAILURE_MODES = {
    "NORMAL": "normal",
    "TRANSIENT": "transient_failure",
    "PERSISTENT": "persistent_failure",
    "PRIMARY_DOWN": "primary_model_down",
    "REGION_DOWN": "region_down",
}

PRIMARY_MODEL = "primary-model"
FALLBACK_MODEL = "fallback-model"

MAX_RETRIES = 3

BASE_BACKOFF_SECONDS = 0.1

CIRCUIT_FAILURE_THRESHOLD = 3

CIRCUIT_RECOVERY_TIMEOUT = 1.0