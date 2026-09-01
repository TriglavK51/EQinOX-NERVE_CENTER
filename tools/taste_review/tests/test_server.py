from tools.taste_review.server import run


def test_review_flags_static_design_smells() -> None:
    result = run({"text": "<div><p>Content</p></div><style>p { font-family: Arial; }</style>"})

    assert result["localOnly"] is True
    assert {finding["code"] for finding in result["report"]["findings"]} >= {
        "missing_main",
        "missing_h1",
        "generic_font",
    }


def test_review_accepts_semantic_accessible_input() -> None:
    document = """
    <main><h1>Purposeful page</h1><p>Content</p></main>
    <style>@media (prefers-reduced-motion: reduce) { * { animation: none; } }</style>
    """

    assert run({"text": document})["report"]["score"] == 100
