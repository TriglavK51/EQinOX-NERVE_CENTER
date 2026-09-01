import json
from types import SimpleNamespace

from tools.cra_evidence_pack import server


def test_run_generates_and_verifies_local_evidence_pack(tmp_path, monkeypatch):
    sbom_path = tmp_path / "bom.json"
    product_path = tmp_path / "product.yaml"
    output_path = tmp_path / "evidence"
    sbom_path.write_text("{}", encoding="utf-8")
    product_path.write_text("id: example", encoding="utf-8")
    monkeypatch.setattr(server, "_find_executable", lambda: "cra-sbom")

    def fake_run(command, **_):
        if command[1] == "evidence":
            assert "--vex" not in command
            output_path.mkdir()
            (output_path / "cra_evidence.json").write_text(
                json.dumps({"findings": [{}], "art14_notification_drafts": []}), encoding="utf-8"
            )
            (output_path / "audit.sha256").write_text("hash", encoding="utf-8")
        else:
            assert command[1:] == ["verify", "--evidence-pack", str(output_path)]
        return SimpleNamespace(returncode=0, stderr="")

    monkeypatch.setattr(server.subprocess, "run", fake_run)

    result = server.run(
        {
            "sbomPath": str(sbom_path),
            "productManifestPath": str(product_path),
            "outputPath": str(output_path),
        }
    )

    assert result["status"] == "ok"
    assert result["localOnly"] is True
    assert result["findingCount"] == 1
    assert result["auditChainVerified"] is True


def test_run_requires_existing_absolute_sbom_path(tmp_path):
    product_path = tmp_path / "product.yaml"
    product_path.write_text("id: example", encoding="utf-8")

    try:
        server.run(
            {
                "sbomPath": "bom.json",
                "productManifestPath": str(product_path),
                "outputPath": str(tmp_path / "out"),
            }
        )
    except ValueError as error:
        assert str(error) == "input.sbomPath must be an absolute path"
    else:
        raise AssertionError("relative SBOM paths must be rejected")
