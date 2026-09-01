"""Local EU CRA evidence-pack generation through the cra-sbom CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from tools._common import meta

NAME = "cra_evidence_pack"


def run(input_data: dict) -> dict:
    """Generate and verify a hash-chained CRA evidence pack from local input files."""
    sbom_path = _required_absolute_file(input_data, "sbomPath")
    product_path = _required_absolute_file(input_data, "productManifestPath")
    output_path = _required_absolute_path(input_data, "outputPath")
    vex_path = _optional_absolute_file(input_data, "vexPath")
    executable = _find_executable()
    if executable is None:
        return {
            "status": "unavailable",
            "localOnly": True,
            "reason": "cra-sbom is not installed or is not available on PATH",
            "install": "pip install cra-sbom-evidence",
        }

    command = [
        executable,
        "evidence",
        "--sbom",
        str(sbom_path),
        "--product",
        str(product_path),
        "--out",
        str(output_path),
    ]
    if vex_path is not None:
        command.extend(["--vex", str(vex_path)])
    completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=60)
    if completed.returncode != 0:
        return _command_error(completed)

    evidence_path = output_path / "cra_evidence.json"
    audit_path = output_path / "audit.sha256"
    if not evidence_path.is_file() or not audit_path.is_file():
        return {
            "status": "error",
            "localOnly": True,
            "reason": "cra-sbom completed without creating a complete evidence pack",
        }
    verified = subprocess.run(
        [executable, "verify", "--evidence-pack", str(output_path)],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if verified.returncode != 0:
        return _command_error(verified)

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    findings = evidence.get("findings", [])
    drafts = evidence.get("art14_notification_drafts", [])
    return {
        "status": "ok",
        "localOnly": True,
        "outputPath": str(output_path),
        "findingCount": len(findings) if isinstance(findings, list) else 0,
        "article14DraftCount": len(drafts) if isinstance(drafts, list) else 0,
        "auditChainVerified": True,
    }


def health() -> dict:
    result = meta(NAME)
    result["available"] = _find_executable() is not None
    return result


def get_meta() -> dict:
    return meta(NAME)


def _find_executable() -> str | None:
    executable = shutil.which("cra-sbom")
    if executable is not None:
        return executable
    local_executable = Path(sys.executable).parent / "cra-sbom.exe"
    return str(local_executable) if local_executable.is_file() else None


def _command_error(completed: subprocess.CompletedProcess[str]) -> dict:
    return {
        "status": "error",
        "localOnly": True,
        "exitCode": completed.returncode,
        "stderr": completed.stderr.strip(),
    }


def _required_absolute_file(input_data: dict, field: str) -> Path:
    path = _required_absolute_path(input_data, field)
    if not path.is_file():
        raise ValueError(f"input.{field} must be an existing file")
    return path


def _optional_absolute_file(input_data: dict, field: str) -> Path | None:
    if field not in input_data or input_data[field] is None:
        return None
    return _required_absolute_file(input_data, field)


def _required_absolute_path(input_data: dict, field: str) -> Path:
    value = input_data.get(field)
    if not isinstance(value, str) or not value:
        raise ValueError(f"input.{field} must be a non-empty string")
    path = Path(value)
    if not path.is_absolute():
        raise ValueError(f"input.{field} must be an absolute path")
    return path
