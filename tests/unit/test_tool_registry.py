"""Tests for the manifest boundary used by tool discovery."""

import json

import pytest

from core.tool_registry import ToolManifest, ToolRegistry


def test_registry_discovers_local_tool_manifests():
    catalog = ToolRegistry().catalog()

    assert len(catalog) == 15
    assert set(catalog) >= {"seo_technical", "ponytail_review"}
    assert catalog["seo_technical"].path.name == "tool.json"


def test_manifest_rejects_non_local_tool(tmp_path):
    path = tmp_path / "tool.json"
    source = {
        "name": "remote_tool",
        "version": "1.0.0",
        "description": "Invalid external tool",
        "inputs": {},
        "outputs": {},
        "localOnly": False,
        "permissions": [],
        "costEstimate": "low",
    }
    path.write_text(json.dumps(source), encoding="utf-8")

    with pytest.raises(ValueError, match="localOnly"):
        ToolManifest.from_dict(source, path)
