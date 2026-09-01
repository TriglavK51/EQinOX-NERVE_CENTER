from tools.seo_audit.server import run


def test_run_reports_missing_static_seo_elements():
    result = run(
        {"html": "<html><head><title>Short</title></head><body><h1>One</h1></body></html>"}
    )

    assert result["localOnly"] is True
    assert result["report"]["score"] < 100
    assert {issue["code"] for issue in result["report"]["issues"]} >= {
        "missing_description",
        "missing_language",
        "missing_canonical",
    }


def test_run_accepts_a_complete_static_document():
    html = """<!doctype html><html lang="en"><head>
    <title>A complete example title for search results</title>
    <meta name="description" content="A complete description that is long enough
    for the static audit to accept as search metadata.">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="canonical" href="https://example.test/page">
    <script type="application/ld+json">{}</script>
    </head><body><h1>Example</h1><img src="example.png" alt="Example image"></body></html>"""

    assert run({"html": html})["report"]["score"] == 100
