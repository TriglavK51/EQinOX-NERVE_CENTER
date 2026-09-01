import json
from types import SimpleNamespace

from tools.supply_chain_sbom import server


def test_run_generates_prebuild_sbom_without_dependency_installation(tmp_path, monkeypatch):
    output_path = tmp_path / "bom.json"
    monkeypatch.setattr(server.shutil, "which", lambda _: "cdxgen")

    def fake_run(command, **_):
        assert "--lifecycle" in command
        assert command[command.index("--lifecycle") + 1] == "pre-build"
        assert "--no-install-deps" in command
        output_path.write_text(
            json.dumps({"bomFormat": "CycloneDX", "specVersion": "1.7", "components": [{}]}),
            encoding="utf-8",
        )
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(server.subprocess, "run", fake_run)

    result = server.run({"projectPath": str(tmp_path), "outputPath": str(output_path)})

    assert result == {
        "status": "ok",
        "localOnly": True,
        "outputPath": str(output_path),
        "componentCount": 1,
        "bomFormat": "CycloneDX",
        "specVersion": "1.7",
    }


def test_run_requires_absolute_paths(tmp_path):
    try:
        server.run({"projectPath": ".", "outputPath": str(tmp_path / "bom.json")})
    except ValueError as error:
        assert str(error) == "input.projectPath must be an absolute path"
    else:
        raise AssertionError("relative project paths must be rejected")
