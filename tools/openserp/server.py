"""Free, loopback-only client for a self-hosted OpenSERP instance."""

from __future__ import annotations

import json
from typing import Any
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen

NAME = "openserp"
DEFAULT_BASE_URL = "http://127.0.0.1:7000"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})


def _validate_base_url(value: object) -> str:
    base_url = value if isinstance(value, str) and value else DEFAULT_BASE_URL
    parsed = urlparse(base_url)
    if (
        parsed.scheme not in {"http", "https"}
        or parsed.hostname not in LOOPBACK_HOSTS
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("openserp baseUrl must be an HTTP loopback URL")
    return base_url.rstrip("/")


def run(input_data: dict[str, Any]) -> dict[str, Any]:
    """Query the free, self-hosted OpenSERP API without external egress."""
    if not isinstance(input_data, dict):
        raise ValueError("input_data must be an object")
    query = input_data.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("openserp requires a non-empty query string")
    engines = input_data.get("engines", ["duckduckgo"])
    if not isinstance(engines, list) or not all(isinstance(engine, str) for engine in engines):
        raise ValueError("openserp engines must be an array of strings")
    limit = input_data.get("limit", 10)
    if not isinstance(limit, int) or not 1 <= limit <= 50:
        raise ValueError("openserp limit must be an integer from 1 to 50")

    base_url = _validate_base_url(input_data.get("baseUrl"))
    parameters = {"text": query.strip(), "engines": ",".join(engines), "limit": limit}
    endpoint = f"{base_url}/mega/search?{urlencode(parameters)}"
    with urlopen(endpoint, timeout=10) as response:  # noqa: S310 - host is validated as loopback.
        result = json.loads(response.read().decode("utf-8"))
    if not isinstance(result, dict):
        raise RuntimeError("openserp returned a non-object response")
    return {
        "status": "ok",
        "result": result,
        "connection": {"type": "free_local_api", "baseUrl": base_url},
        "localOnly": True,
    }


def health() -> dict[str, Any]:
    return {"name": NAME, "status": "ready", "localOnly": True}


def get_meta() -> dict[str, Any]:
    return health()
