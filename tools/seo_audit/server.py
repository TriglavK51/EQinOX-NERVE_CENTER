from __future__ import annotations

from html.parser import HTMLParser
from typing import Any

NAME = "seo_audit"


class AuditParser(HTMLParser):
    """Collect metadata needed for a deterministic, offline HTML audit."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.canonical = ""
        self.language = ""
        self.h1_count = 0
        self.images_without_alt = 0
        self.has_viewport = False
        self.has_schema = False
        self.has_robots = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {name.lower(): (value or "") for name, value in attrs}
        if tag == "html":
            self.language = attributes.get("lang", "").strip()
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attributes.get("name", "").lower()
            if name == "description":
                self.description = attributes.get("content", "").strip()
            elif name == "viewport":
                self.has_viewport = True
            elif name == "robots":
                self.has_robots = True
        elif tag == "link" and attributes.get("rel", "").lower() == "canonical":
            self.canonical = attributes.get("href", "").strip()
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img" and not attributes.get("alt", "").strip():
            self.images_without_alt += 1
        elif tag == "script" and attributes.get("type", "").lower() == "application/ld+json":
            self.has_schema = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def audit_html(html: str) -> dict[str, Any]:
    """Check SEO-relevant static HTML without network or browser access."""
    parser = AuditParser()
    parser.feed(html)
    issues: list[dict[str, str]] = []

    def require(condition: bool, code: str, message: str) -> None:
        if not condition:
            issues.append({"code": code, "severity": "warning", "message": message})

    require(bool(parser.title), "missing_title", "Document has no title element.")
    require(
        10 <= len(parser.title) <= 60, "title_length", "Title should contain 10 to 60 characters."
    )
    require(bool(parser.description), "missing_description", "Document has no meta description.")
    require(
        not parser.description or 50 <= len(parser.description) <= 160,
        "description_length",
        "Meta description should contain 50 to 160 characters.",
    )
    require(bool(parser.language), "missing_language", "HTML element has no lang attribute.")
    require(parser.h1_count == 1, "h1_count", "Document should contain exactly one H1 element.")
    require(bool(parser.canonical), "missing_canonical", "Document has no canonical link.")
    require(
        parser.has_viewport, "missing_viewport", "Document has no responsive viewport meta tag."
    )
    require(parser.has_schema, "missing_schema", "Document has no JSON-LD structured data.")
    require(parser.images_without_alt == 0, "image_alt", "One or more images have no alt text.")

    return {
        "score": max(0, 100 - 10 * len(issues)),
        "checks": 10,
        "issues": issues,
        "metadata": {
            "title": parser.title,
            "description": parser.description,
            "canonical": parser.canonical,
            "language": parser.language,
            "h1Count": parser.h1_count,
        },
    }


def run(input_data: dict) -> dict:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    html = input_data.get("html")
    if not isinstance(html, str) or not html.strip():
        raise ValueError("seo_audit requires a non-empty html string")
    return {"status": "ok", "report": audit_html(html), "localOnly": True}


def health() -> dict:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict:
    return health()
