"""Validation, routing, audited execution, and local result aggregation."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
from typing import Any

from core.api_adapter import run_tool
from core.chain_builder import build_chain
from core.evolution import record_dispatch
from core.fallbacks import RetryPolicy
from core.scoring import ToolScore, calculate_score
from core.tool_registry import ToolRegistry
from core.utils import load_config, project_path


class Dispatcher:
    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.config = load_config()
        self.retry = RetryPolicy()
        self.registry = registry or ToolRegistry()

    def manifests(self) -> list[dict[str, Any]]:
        return [manifest.as_dict() for manifest in self.registry.list()]

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        tool = request.get("tool")
        input_data = request.get("input", {})
        agent = request.get("agent", "local")
        if not isinstance(tool, str) or not tool:
            raise ValueError("field 'tool' must be a non-empty string")
        if not isinstance(input_data, dict) or not isinstance(agent, str):
            raise ValueError("fields 'input' and 'agent' must be objects and strings respectively")
        catalog = self.registry.catalog()
        available = set(catalog)
        if tool == "chain":
            chain = build_chain(
                str(input_data.get("intent", "")), available, int(self.config["chainMaxDepth"])
            )
            if not chain:
                raise ValueError("no executable chain matches input.intent")
        elif tool in available:
            chain = [tool]
        else:
            raise ValueError(f"unknown tool: {tool}")
        started = time.perf_counter()
        results: dict[str, Any] = {}
        try:
            for name in chain:
                results[name] = self.retry.call(name, lambda name=name: run_tool(name, input_data))
                record_dispatch(name, True)
            payload = {"status": "ok", "tool": tool, "chain": chain, "results": results}
        except Exception:
            record_dispatch(chain[-1], False)
            raise
        payload["score"] = calculate_score(
            ToolScore(1.0, 0.0, 1.0, 1.0), self.config["scoringWeights"]
        )
        payload["latencyMs"] = round((time.perf_counter() - started) * 1000, 2)
        self._audit(agent, tool, input_data, payload)
        return payload

    def _audit(
        self, agent: str, tool: str, input_data: dict[str, Any], output: dict[str, Any]
    ) -> None:
        def digest(value: Any) -> str:
            encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
            return hashlib.sha256(encoded).hexdigest()

        entry = {
            "agent": agent,
            "tool": tool,
            "inputHash": digest(input_data),
            "outputHash": digest(output),
        }
        key = os.environ.get("NERVE_CENTER_AUDIT_KEY", "local-audit-key").encode()
        entry["signature"] = hmac.new(
            key, json.dumps(entry, sort_keys=True).encode(), hashlib.sha256
        ).hexdigest()
        path = project_path("logs", "audit.log")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")
