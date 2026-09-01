from unittest.mock import patch

import pytest

from core.dispatcher import Dispatcher


def test_dispatch_seo_technical() -> None:
    result = Dispatcher().dispatch(
        {"tool": "seo_technical", "input": {"html": "<title>X</title><h1>Y</h1>"}}
    )
    assert result["status"] == "ok"
    assert result["results"]["seo_technical"]["report"]["title"] == "X"


def test_dispatch_rejects_an_unknown_tool() -> None:
    with pytest.raises(ValueError, match="unknown tool"):
        Dispatcher().dispatch({"tool": "unknown", "input": {}})


def test_dispatch_runs_a_category_in_parallel() -> None:
    result = Dispatcher().dispatch(
        {"tool": "category", "input": {"category": "seo", "html": "<title>X</title><h1>Y</h1>"}}
    )

    assert result["status"] == "ok"
    assert result["localOnly"] is True
    assert result["chain"] == [
        "seo_audit",
        "seo_drift",
        "seo_schema",
        "seo_technical",
        "seo_unlighthouse",
    ]
    assert result["results"]["seo_technical"]["report"]["title"] == "X"


@pytest.mark.parametrize(
    ("category", "input_data"),
    [
        (
            "seo",
            {
                "html": (
                    "<html><head><title>Example title</title></head>"
                    "<body><h1>X</h1></body></html>"
                )
            },
        ),
        ("geo", {"text": "Local GEO review"}),
        ("crawling", {"html": "<html><body><h1>X</h1></body></html>"}),
        ("security", {"text": "Review this input"}),
        ("writing", {"text": "Create an offline report"}),
        ("token_optimization", {"text": "Simplify this prompt"}),
        ("code_quality", {"text": "Review this function"}),
        ("devops", {"text": "Inspect this image manifest"}),
        ("taste", {"text": "<main><h1>Purposeful page</h1></main>"}),
    ],
)
def test_each_category_dispatches_its_local_tools(category, input_data) -> None:
    result = Dispatcher().dispatch(
        {"tool": "category", "input": {"category": category, **input_data}}
    )

    assert result["chain"]
    assert all(output["localOnly"] is True for output in result["results"].values())


def test_dispatches_the_serp_category_through_its_local_api_adapter() -> None:
    with patch("core.dispatcher.run_tool", return_value={"status": "ok", "localOnly": True}):
        result = Dispatcher().dispatch({"tool": "category", "input": {"category": "serp"}})

    assert result["chain"] == ["openserp"]
    assert result["results"]["openserp"]["localOnly"] is True
