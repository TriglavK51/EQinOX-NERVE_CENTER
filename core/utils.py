"""Small filesystem and JSON helpers for the local service."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def project_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
    temporary.replace(path)


def load_config() -> dict[str, Any]:
    return load_json(project_path("mcp.json"), {})


def get_logger(name: str) -> logging.Logger:
    log_path = project_path("logs", "app.log")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
