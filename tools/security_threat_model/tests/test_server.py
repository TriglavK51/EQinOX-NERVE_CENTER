from tools.security_threat_model.server import run


def test_run_is_local():
    assert run({})["localOnly"] is True
