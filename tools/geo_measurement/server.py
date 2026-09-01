"""Deterministic aggregation of operator-provided GEO probe data."""

from __future__ import annotations

from typing import Any

NAME = "geo_measurement"


def measure_visibility(probes: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate reproducible mention and citation rates from completed probes."""
    total = len(probes)
    mentioned = sum(probe.get("mentioned") is True for probe in probes)
    cited = sum(probe.get("cited") is True for probe in probes)
    return {
        "probeCount": total,
        "mentionRate": round(mentioned / total * 100, 2),
        "citationRate": round(cited / total * 100, 2),
        "score": round((mentioned + cited) / (2 * total) * 100, 2),
    }


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    probes = input_data.get("probes")
    if (
        not isinstance(probes, list)
        or not probes
        or not all(isinstance(probe, dict) for probe in probes)
    ):
        raise ValueError("geo_measurement requires a non-empty probes array of objects")
    return {"status": "ok", "report": measure_visibility(probes), "localOnly": True}


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
