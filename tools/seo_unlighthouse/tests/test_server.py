from tools.seo_unlighthouse.server import run


def test_run_is_local():
    assert run({})["localOnly"] is True
