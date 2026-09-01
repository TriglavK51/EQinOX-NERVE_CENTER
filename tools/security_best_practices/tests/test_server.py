from tools.security_best_practices.server import run


def test_run_is_local():
    assert run({})["localOnly"] is True
