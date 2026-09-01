"""Shared deterministic implementations for offline tool adapters."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Any


class PageSummary(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.headings: list[str] = []
        self.links = 0
        self._in_title = False
        self._heading: str | None = None

    def handle_starttag(self, tag: str, _attrs: list[tuple[str, str | None]]) -> None:
        self._in_title = tag == "title"
        self._heading = tag if tag in {"h1", "h2", "h3"} else None
        if tag == "a":
            self.links += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == self._heading:
            self._heading = None

    def handle_data(self, data: str) -> None:
        value = data.strip()
        if self._in_title and value:
            self.title += value
        if self._heading and value:
            self.headings.append(value)


def analyze_page(input_data: dict[str, Any]) -> dict[str, Any]:
    html = str(input_data.get("html") or input_data.get("text") or "")
    if not html:
        fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "sample_page.html"
        html = (
            fixture.read_text(encoding="utf-8")
            if fixture.exists()
            else "<html><head><title>Empty</title></head></html>"
        )
    parser = PageSummary()
    parser.feed(html)
    warnings: list[str] = []
    if not parser.title:
        warnings.append("missing title")
    if not parser.headings:
        warnings.append("missing headings")
    return {
        "title": parser.title,
        "headings": parser.headings,
        "linkCount": parser.links,
        "warnings": warnings,
    }


def run_local_tool(name: str, input_data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    if name == "seo_technical":
        report = analyze_page(input_data)
        report["score"] = max(0, 100 - 25 * len(report["warnings"]))
        return {"status": "ok", "report": report, "localOnly": True}
    if name == "pdf":
        return {
            "status": "ok",
            "document": {"format": "json-fallback", "content": input_data},
            "localOnly": True,
        }
    return {
        "status": "ok",
        "tool": name,
        "result": {"inputKeys": sorted(input_data), "mode": "offline-stub"},
        "localOnly": True,
    }


def meta(name: str) -> dict[str, Any]:
    return {"name": name, "status": "ready", "localOnly": True}
