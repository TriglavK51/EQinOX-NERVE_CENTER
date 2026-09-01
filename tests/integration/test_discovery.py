from core.dispatcher import Dispatcher


def test_discovery_contains_all_tools() -> None:
    names = {item["name"] for item in Dispatcher().manifests()}
    assert len(names) == 23
    assert "seo_technical" in names
    assert "supply_chain_sbom" in names
    assert "cra_evidence_pack" in names
