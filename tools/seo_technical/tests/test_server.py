from tools.seo_technical.server import run


def test_report_contains_title():
    assert run({"html": "<title>A</title><h1>B</h1>"})["report"]["title"] == "A"
