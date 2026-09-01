from tools.pdf.server import run


def test_returns_structured_fallback():
    assert run({})["document"]["format"] == "json-fallback"
