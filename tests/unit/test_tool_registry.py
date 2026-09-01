"""Tests for the manifest boundary used by tool discovery."""

import json

import pytest

from core.tool_registry import ToolManifest, ToolRegistry


def test_registry_discovers_local_tool_manifests():
    catalog = ToolRegistry().catalog()

    assert len(catalog) == 21
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


def test_registry_returns_all_tools_in_a_category(tmp_path):
    for name in ("seo_a", "seo_b"):
        tool_dir = tmp_path / name
        tool_dir.mkdir()
        (tool_dir / "tool.json").write_text(
            json.dumps(
                {
                    "name": name,
                    "category": "seo",
                    "version": "1.2.0",
                    "description": "Local SEO check",
                    "inputs": {},
                    "outputs": {},
                    "localOnly": True,
                    "permissions": [],
                    "costEstimate": "low",
                }
            ),
            encoding="utf-8",
        )

    assert [manifest.name for manifest in ToolRegistry(tmp_path).by_category("seo")] == [
        "seo_a",
        "seo_b",
    ]
