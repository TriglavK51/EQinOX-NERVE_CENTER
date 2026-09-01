from core.dispatcher import Dispatcher


def test_dispatch_seo_technical() -> None:
    result = Dispatcher().dispatch(
        {"tool": "seo_technical", "input": {"html": "<title>X</title><h1>Y</h1>"}}
    )
    assert result["status"] == "ok"
    assert result["results"]["seo_technical"]["report"]["title"] == "X"
