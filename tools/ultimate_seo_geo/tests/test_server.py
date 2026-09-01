from tools.ultimate_seo_geo.server import run


def test_run_is_local():
    assert run({})["localOnly"] is True
