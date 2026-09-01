from unittest.mock import MagicMock, patch

import pytest

from tools.openserp.server import run


def test_run_uses_the_free_loopback_api() -> None:
    response = MagicMock()
    response.read.return_value = b'{"results": []}'
    with patch("tools.openserp.server.urlopen") as mocked_urlopen:
        mocked_urlopen.return_value.__enter__.return_value = response
        result = run({"query": "local SEO", "engines": ["duckduckgo"], "limit": 5})

    assert result["connection"] == {"type": "free_local_api", "baseUrl": "http://127.0.0.1:7000"}
    assert result["result"] == {"results": []}
    assert "text=local+SEO" in mocked_urlopen.call_args.args[0]


def test_run_rejects_external_api_hosts() -> None:
    with pytest.raises(ValueError, match="loopback"):
        run({"query": "local SEO", "baseUrl": "https://openserp.org"})
