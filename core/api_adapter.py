"""Safe in-process adapter for local tool server modules."""

from __future__ import annotations

import importlib.util
from types import ModuleType
from typing import Any

from core.utils import project_path


def load_tool_module(tool_name: str) -> ModuleType:
    if not tool_name.replace("_", "").isalnum() or "/" in tool_name or "\\" in tool_name:
        raise ValueError("invalid tool name")
    path = project_path("tools", tool_name, "server.py").resolve()
    tools_root = project_path("tools").resolve()
    if tools_root not in path.parents or not path.is_file():
        raise ValueError(f"unknown local tool: {tool_name}")
    spec = importlib.util.spec_from_file_location(f"nerve_tool_{tool_name}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load tool: {tool_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_tool(tool_name: str, input_data: dict[str, Any]) -> dict[str, Any]:
    module = load_tool_module(tool_name)
    runner = getattr(module, "run", None)
    if not callable(runner):
        raise RuntimeError(f"tool '{tool_name}' does not expose run(input_data)")
    result = runner(input_data)
    if not isinstance(result, dict):
        raise RuntimeError(f"tool '{tool_name}' returned non-object output")
    return result
