"""Deterministic local checks for answer-engine citability."""

from __future__ import annotations

import re
from typing import Any

NAME = "geo_citability"


def assess_citability(text: str) -> dict[str, Any]:
    """Score independently verifiable, answer-first content signals."""
    paragraphs = [
        paragraph.strip() for paragraph in re.split(r"\n\s*\n", text) if paragraph.strip()
    ]
    sentences = re.split(r"[.!?]+", text)
    findings: list[dict[str, str]] = []

    def require(condition: bool, code: str, message: str) -> None:
        if not condition:
            findings.append({"code": code, "severity": "warning", "message": message})

    require(
        bool(re.search(r"^.{0,280}[.!?]", text, re.DOTALL)),
        "no_direct_answer",
        "Start with a concise direct answer.",
    )
    require("?" in text, "no_question_coverage", "Include the question the content answers.")
    require(
        bool(
            re.search(r"\b\d+(?:[.,]\d+)?(?:%|\s+(?:minutes?|days?|years?|users?))\b", text, re.I)
        ),
        "no_specific_evidence",
        "Support claims with specific, attributable facts.",
    )
    require(
        any(len(sentence.split()) <= 30 for sentence in sentences if sentence.strip()),
        "dense_sentences",
        "Use concise sentences for extraction.",
    )
    require(len(paragraphs) >= 2, "low_structure", "Split the explanation into focused paragraphs.")
    return {"score": max(0, 100 - 20 * len(findings)), "checks": 5, "findings": findings}


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    text = input_data.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("geo_citability requires a non-empty text string")
    return {"status": "ok", "report": assess_citability(text), "localOnly": True}


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
