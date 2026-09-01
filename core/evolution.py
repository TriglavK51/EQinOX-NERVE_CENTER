"""Persist minimal dispatch history and review it every ten calls."""

from __future__ import annotations

from typing import Any

from core.utils import load_json, project_path, save_json

STATE_PATH = project_path("state", "evolution.json")


def record_dispatch(tool: str, succeeded: bool) -> dict[str, Any]:
    state = load_json(STATE_PATH, {"dispatches": 0, "tools": {}, "reviews": 0})
    state["dispatches"] += 1
    stats = state["tools"].setdefault(tool, {"success": 0, "failure": 0})
    stats["success" if succeeded else "failure"] += 1
    if state["dispatches"] % 10 == 0:
        state["reviews"] += 1
        save_json(project_path("state", "snapshots", f"review-{state['dispatches']}.json"), state)
    save_json(STATE_PATH, state)
    return state


def rollback(snapshot: str) -> None:
    source = project_path("state", "snapshots", f"{snapshot}.json")
    if not source.is_file():
        raise ValueError("unknown snapshot")
    save_json(STATE_PATH, load_json(source))
