"""Local discovery and validation of tool manifests.

New tools are discovered from ``tools/<name>/tool.json``. The registry keeps
manifest parsing and the public tool contract out of the dispatcher.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from core.utils import load_json, project_path

REQUIRED_FIELDS = frozenset(
    {
        "name",
        "version",
        "description",
        "inputs",
        "outputs",
        "localOnly",
        "permissions",
        "costEstimate",
    }
)


@dataclass(frozen=True)
class ToolManifest:
    """Validated, local-only tool metadata."""

    name: str
    version: str
    description: str
    inputs: dict[str, str]
    outputs: dict[str, str]
    permissions: tuple[str, ...]
    cost_estimate: str
    path: Path

    @classmethod
    def from_dict(cls, source: dict[str, Any], path: Path) -> "ToolManifest":
        missing = REQUIRED_FIELDS.difference(source)
        if missing:
            raise ValueError(f"manifest {path} is missing: {', '.join(sorted(missing))}")
        if source["localOnly"] is not True:
            raise ValueError(f"manifest {path} must set localOnly to true")
        if not isinstance(source["name"], str) or not source["name"].replace("_", "").isalnum():
            raise ValueError(f"manifest {path} has an invalid name")
        if not isinstance(source["inputs"], dict) or not isinstance(source["outputs"], dict):
            raise ValueError(f"manifest {path} inputs and outputs must be objects")
        if not isinstance(source["permissions"], list) or not all(
            isinstance(permission, str) for permission in source["permissions"]
        ):
            raise ValueError(f"manifest {path} permissions must be a list of strings")
        return cls(
            name=source["name"],
            version=str(source["version"]),
            description=str(source["description"]),
            inputs={key: str(value) for key, value in source["inputs"].items()},
            outputs={key: str(value) for key, value in source["outputs"].items()},
            permissions=tuple(source["permissions"]),
            cost_estimate=str(source["costEstimate"]),
            path=path,
        )

    def as_dict(self) -> dict[str, Any]:
        """Return API-compatible manifest metadata."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "localOnly": True,
            "permissions": list(self.permissions),
            "costEstimate": self.cost_estimate,
        }


class ToolRegistry:
    """Discover tool manifests from the local tools directory."""

    def __init__(self, tools_root: Path | None = None) -> None:
        self.tools_root = tools_root or project_path("tools")

    def list(self) -> list[ToolManifest]:
        return list(self.catalog().values())

    def catalog(self) -> dict[str, ToolManifest]:
        """Return all discovered tools indexed by their unique public name."""
        catalog: dict[str, ToolManifest] = {}
        for path in sorted(self.tools_root.glob("*/tool.json")):
            manifest = self._read(path)
            if manifest.name in catalog:
                raise ValueError("tool manifest names must be unique")
            catalog[manifest.name] = manifest
        return catalog

    def names(self) -> set[str]:
        return set(self.catalog())

    def require(self, name: str) -> ToolManifest:
        try:
            return self.catalog()[name]
        except KeyError as error:
            raise ValueError(f"unknown tool: {name}") from error

    @staticmethod
    def _read(path: Path) -> ToolManifest:
        document = load_json(path)
        if not isinstance(document, dict):
            raise ValueError(f"manifest {path} must be a JSON object")
        return ToolManifest.from_dict(document, path)
