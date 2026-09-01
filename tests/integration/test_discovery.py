from core.dispatcher import Dispatcher


def test_discovery_contains_all_tools() -> None:
    names = {item["name"] for item in Dispatcher().manifests()}
    assert len(names) == 17
    assert "seo_technical" in names
