import asyncio
import random
import time
from enum import Enum
from typing import Callable, Awaitable, Any


class CircuitState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 1.0,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def can_execute(self):

        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:

            if time.time() - self.opened_at >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                return True

            return False

        return True

    def record_success(self):

        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.opened_at = None

    def record_failure(self):

        self.failure_count += 1

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.opened_at = time.time()


async def retry_with_backoff(
    operation: Callable[[], Awaitable[Any]],
    max_retries: int = 3,
    base_delay: float = 0.1,
    jitter: float = 0.05,
    circuit_breaker: CircuitBreaker | None = None,
):

    attempts = 0
    delays = []

    while True:

        if circuit_breaker and not circuit_breaker.can_execute():

            return {
                "success": False,
                "error": "Circuit breaker is OPEN",
                "error_type": "CircuitOpen",
                "attempts": attempts,
                "retry_count": attempts,
                "retry_delays": delays,
                "circuit_state": circuit_breaker.state.value,
            }

        try:

            result = await operation()

            if circuit_breaker:
                circuit_breaker.record_success()

            return {
                "success": True,
                "result": result,
                "attempts": attempts + 1,
                "retry_count": attempts,
                "retry_delays": delays,
                "circuit_state": (
                    circuit_breaker.state.value
                    if circuit_breaker
                    else None
                ),
            }

        except Exception as exc:

            if circuit_breaker:
                circuit_breaker.record_failure()

            if attempts >= max_retries:

                return {
                    "success": False,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "attempts": attempts + 1,
                    "retry_count": attempts,
                    "retry_delays": delays,
                    "circuit_state": (
                        circuit_breaker.state.value
                        if circuit_breaker
                        else None
                    ),
                }

            delay = (
                base_delay * (2 ** attempts)
                + random.uniform(0, jitter)
            )

            delays.append(round(delay, 4))

            attempts += 1

            await asyncio.sleep(delay)