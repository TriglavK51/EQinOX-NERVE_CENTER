"""Local, pre-build CycloneDX SBOM generation through the cdxgen CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from tools._common import meta

NAME = "supply_chain_sbom"


def run(input_data: dict) -> dict:
    """Generate an SBOM without installing project dependencies or using network services."""
    project_path = _required_absolute_path(input_data, "projectPath", must_be_directory=True)
    output_path = _required_absolute_path(input_data, "outputPath", must_be_directory=False)
    executable = shutil.which("cdxgen")
    if executable is None:
        return {
            "status": "unavailable",
            "localOnly": True,
            "reason": "cdxgen is not installed or is not available on PATH",
            "install": "npm install --global @cdxgen/cdxgen",
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        executable,
        str(project_path),
        "--lifecycle",
        "pre-build",
        "--no-install-deps",
        "--output",
        str(output_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=300)
    if completed.returncode != 0:
        return {
            "status": "error",
            "localOnly": True,
            "exitCode": completed.returncode,
            "stderr": completed.stderr.strip(),
        }
    if not output_path.is_file():
        return {
            "status": "error",
            "localOnly": True,
            "reason": "cdxgen completed without creating the requested SBOM",
        }

    bom = json.loads(output_path.read_text(encoding="utf-8"))
    components = bom.get("components", [])
    return {
        "status": "ok",
        "localOnly": True,
        "outputPath": str(output_path),
        "componentCount": len(components) if isinstance(components, list) else 0,
        "bomFormat": bom.get("bomFormat"),
        "specVersion": bom.get("specVersion"),
    }


def health() -> dict:
    result = meta(NAME)
    result["available"] = shutil.which("cdxgen") is not None
    return result


def get_meta() -> dict:
    return meta(NAME)


def _required_absolute_path(input_data: dict, field: str, *, must_be_directory: bool) -> Path:
    value = input_data.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"input.{field} must be a non-empty string")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"input.{field} must be an absolute path")
    if must_be_directory and not path.is_dir():
        raise ValueError(f"input.{field} must be an existing directory")
    return path
