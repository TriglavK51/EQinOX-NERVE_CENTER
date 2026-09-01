"""Local llms.txt hygiene checks."""

from __future__ import annotations

from typing import Any

NAME = "geo_llmstxt"


def validate_llms_txt(text: str) -> dict[str, Any]:
    """Validate essential facts and Markdown structure for an llms.txt file."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    findings: list[dict[str, str]] = []

    def require(condition: bool, code: str, message: str) -> None:
        if not condition:
            findings.append({"code": code, "severity": "warning", "message": message})

    require(bool(lines and lines[0].startswith("# ")), "missing_title", "Start with one H1 title.")
    require(
        any(line.startswith("> ") for line in lines),
        "missing_summary",
        "Add a concise summary block.",
    )
    require(
        any(line.startswith("## ") for line in lines),
        "missing_sections",
        "Group resources under H2 headings.",
    )
    require(
        any("](http" in line for line in lines), "missing_links", "Link to canonical source pages."
    )
    require(len(text) <= 20_000, "too_large", "Keep llms.txt concise and focused.")
    return {"score": max(0, 100 - 20 * len(findings)), "checks": 5, "findings": findings}


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    text = input_data.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("geo_llmstxt requires a non-empty text string")
    return {"status": "ok", "report": validate_llms_txt(text), "localOnly": True}


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
