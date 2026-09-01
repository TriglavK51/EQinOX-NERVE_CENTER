from tools.geo_measurement.server import run


def test_measurement_aggregates_probe_results() -> None:
    result = run(
        {"probes": [{"mentioned": True, "cited": True}, {"mentioned": True, "cited": False}]}
    )

    assert result["report"] == {
        "probeCount": 2,
        "mentionRate": 100.0,
        "citationRate": 50.0,
        "score": 75.0,
    }
