from tools.geo_citability.server import run


def test_citability_flags_unstructured_claims() -> None:
    result = run({"text": "Our service is the best choice for teams."})

    assert result["report"]["score"] < 100
    assert {finding["code"] for finding in result["report"]["findings"]} >= {
        "no_question_coverage",
        "no_specific_evidence",
        "low_structure",
    }


def test_citability_accepts_answer_first_evidence() -> None:
    text = (
        "What is the result? The process reduced review time by 25% in 30 days.\n\n"
        "It uses a documented local workflow."
    )

    assert run({"text": text})["report"]["score"] == 100
