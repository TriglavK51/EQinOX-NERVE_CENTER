"""Retry and circuit-breaker primitives without external dependencies."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

T = TypeVar("T")


@dataclass
class CircuitBreaker:
    failure_limit: int = 3
    reset_seconds: float = 30.0
    failures: int = 0
    opened_at: float | None = None

    def allow(self) -> bool:
        if self.opened_at is None:
            return True
        if time.monotonic() - self.opened_at >= self.reset_seconds:
            self.failures = 0
            self.opened_at = None
            return True
        return False

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_limit:
            self.opened_at = time.monotonic()


@dataclass
class RetryPolicy:
    attempts: int = 2
    breakers: dict[str, CircuitBreaker] = field(default_factory=dict)

    def call(self, name: str, operation: Callable[[], T]) -> T:
        breaker = self.breakers.setdefault(name, CircuitBreaker())
        if not breaker.allow():
            raise RuntimeError(f"tool '{name}' circuit is open")
        last_error: Exception | None = None
        for _ in range(self.attempts):
            try:
                result = operation()
                breaker.record_success()
                return result
            except Exception as error:
                last_error = error
                breaker.record_failure()
        raise RuntimeError(f"tool '{name}' failed after retries: {last_error}") from last_error
