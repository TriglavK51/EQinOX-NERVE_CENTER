"""Deterministic local review for baseline frontend design quality."""

from __future__ import annotations

from typing import Any

NAME = "taste_review"


def review_frontend(text: str) -> dict[str, Any]:
    """Report static quality signals without rendering, APIs, or network access."""
    normalized = text.lower()
    findings: list[dict[str, str]] = []

    def flag(condition: bool, code: str, message: str) -> None:
        if condition:
            findings.append({"code": code, "severity": "warning", "message": message})

    flag("<main" not in normalized, "missing_main", "Use a main landmark for primary content.")
    flag("<h1" not in normalized, "missing_h1", "Use one clear H1 for page hierarchy.")
    flag(
        any(font in normalized for font in ("font-family: arial", "font-family: roboto")),
        "generic_font",
        "Choose a deliberate typeface instead of a generic default.",
    )
    flag(
        normalized.count("linear-gradient(") > 2,
        "gradient_overuse",
        "Limit gradients so they support the visual hierarchy.",
    )
    flag(
        "animation:" in normalized and "prefers-reduced-motion" not in normalized,
        "motion_accessibility",
        "Respect reduced-motion preferences when using animation.",
    )
    return {"score": max(0, 100 - 20 * len(findings)), "checks": 5, "findings": findings}


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    text = input_data.get("text") or input_data.get("html") or ""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("taste_review requires a non-empty text or html string")
    return {"status": "ok", "report": review_frontend(text), "localOnly": True}


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
