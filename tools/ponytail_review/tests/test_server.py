from tools.ponytail_review.server import run


def test_run_is_local():
    assert run({})["localOnly"] is True
