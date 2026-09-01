"""Stdlib HTTP API for the local Nerve Center tool catalog."""

from __future__ import annotations

import json
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from core.dispatcher import Dispatcher
from core.utils import load_config

METRICS = {"dispatches": 0, "errors": 0, "latency_ms": 0.0}


class Handler(BaseHTTPRequestHandler):
    dispatcher = Dispatcher()

    def log_message(self, _format: str, *_args: object) -> None:
        return

    def _json(self, status: HTTPStatus, body: dict[str, Any]) -> None:
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._json(HTTPStatus.OK, {"status": "ok", "localOnly": True})
        elif self.path == "/.well-known/tools":
            self._json(HTTPStatus.OK, {"tools": self.dispatcher.manifests()})
        elif self.path == "/metrics":
            count = METRICS["dispatches"]
            average = METRICS["latency_ms"] / count if count else 0.0
            metrics = "\n".join(
                (
                    f"nerve_center_dispatches_total {count}",
                    f"nerve_center_errors_total {METRICS['errors']}",
                    f"nerve_center_dispatch_latency_ms_average {average:.2f}",
                    "",
                )
            )
            encoded = metrics.encode()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
        else:
            self._json(HTTPStatus.NOT_FOUND, {"status": "error", "error": "endpoint not found"})

    def do_POST(self) -> None:
        if self.path != "/run":
            self._json(HTTPStatus.NOT_FOUND, {"status": "error", "error": "endpoint not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("request body must be between 1 and 1000000 bytes")
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict):
                raise ValueError("request body must be a JSON object")
            started = time.perf_counter()
            result = self.dispatcher.dispatch(request)
            METRICS["dispatches"] += 1
            METRICS["latency_ms"] += (time.perf_counter() - started) * 1000
            self._json(HTTPStatus.OK, result)
        except (ValueError, json.JSONDecodeError) as error:
            METRICS["errors"] += 1
            self._json(HTTPStatus.BAD_REQUEST, {"status": "error", "error": str(error)})
        except Exception:
            METRICS["errors"] += 1
            self._json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"status": "error", "error": "local tool execution failed"},
            )


def main() -> None:
    config = load_config()
    host = str(config.get("host", "127.0.0.1"))
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("mcp server may only bind to localhost")
    server = ThreadingHTTPServer((host, int(config.get("port", 8088))), Handler)
    print(f"Nerve Center listening on http://{host}:{server.server_port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
