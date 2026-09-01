"""Tool scoring based on relevance, inverse cost, speed, and track record."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

DEFAULT_WEIGHTS = {
    "relevance": 0.40,
    "cost": 0.25,
    "speed": 0.20,
    "trackRecord": 0.15,
}


@dataclass(frozen=True)
class ToolScore:
    """Normalized factors used to rank one candidate tool."""

    relevance: float
    cost: float
    speed: float
    track_record: float = 0.60

    def validate(self) -> None:
        for name, value in self.as_dict().items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be within 0.0 and 1.0")

    def as_dict(self) -> dict[str, float]:
        return {
            "relevance": self.relevance,
            "cost": self.cost,
            "speed": self.speed,
            "trackRecord": self.track_record,
        }


def validate_weights(weights: Mapping[str, float]) -> dict[str, float]:
    """Validate and normalize weights loaded from the local configuration."""
    normalized = {name: float(weights.get(name, DEFAULT_WEIGHTS[name])) for name in DEFAULT_WEIGHTS}
    if any(value < 0.0 for value in normalized.values()):
        raise ValueError("scoring weights cannot be negative")
    if abs(sum(normalized.values()) - 1.0) > 0.0001:
        raise ValueError("scoring weights must sum to 1.0")
    return normalized


def calculate_score(factors: ToolScore, weights: Mapping[str, float] | None = None) -> float:
    """Calculate score, treating lower tool cost as a higher ranking value."""
    factors.validate()
    active_weights = validate_weights(weights or DEFAULT_WEIGHTS)
    return round(
        factors.relevance * active_weights["relevance"]
        + (1.0 - factors.cost) * active_weights["cost"]
        + factors.speed * active_weights["speed"]
        + factors.track_record * active_weights["trackRecord"],
        4,
    )
