from tools.geo_llmstxt.server import run


def test_validator_reports_missing_llms_txt_sections() -> None:
    result = run({"text": "Our product documentation."})

    assert result["report"]["score"] < 100
    assert {finding["code"] for finding in result["report"]["findings"]} >= {
        "missing_title",
        "missing_summary",
        "missing_sections",
        "missing_links",
    }


def test_validator_accepts_structured_llms_txt() -> None:
    text = (
        "# Example\n\n> Local product facts.\n\n## Documentation\n\n"
        "- [Guide](https://example.test/guide)"
    )

    assert run({"text": text})["report"]["score"] == 100
