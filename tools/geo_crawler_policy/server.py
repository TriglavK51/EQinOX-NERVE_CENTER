"""Local inspection of robots.txt rules for well-known AI crawlers."""

from __future__ import annotations

from typing import Any

NAME = "geo_crawler_policy"
AI_CRAWLERS = ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended")


def review_robots_txt(robots_txt: str) -> dict[str, Any]:
    """Identify missing explicit policies and blanket blocks for AI crawlers."""
    lowered = robots_txt.lower()
    findings: list[dict[str, str]] = []
    for crawler in AI_CRAWLERS:
        crawler_name = crawler.lower()
        if f"user-agent: {crawler_name}" not in lowered:
            findings.append(
                {
                    "code": "unspecified_crawler",
                    "severity": "info",
                    "message": f"No explicit policy for {crawler}.",
                }
            )
        elif f"user-agent: {crawler_name}\ndisallow: /" in lowered:
            findings.append(
                {
                    "code": "blocked_crawler",
                    "severity": "warning",
                    "message": f"{crawler} is blocked from the whole site.",
                }
            )
    return {
        "score": max(0, 100 - 10 * len(findings)),
        "checks": len(AI_CRAWLERS),
        "findings": findings,
    }


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    robots_txt = input_data.get("robotsTxt")
    if not isinstance(robots_txt, str):
        raise ValueError("geo_crawler_policy requires a robotsTxt string")
    return {"status": "ok", "report": review_robots_txt(robots_txt), "localOnly": True}


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
