"""Scope: Serve one cabinet GLB through the bundled local review viewer."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Type
import webbrowser

from review_file_resolver import ReviewFileResolver
from review_decision_store import ReviewDecisionStore


class ReviewRequestHandler(BaseHTTPRequestHandler):
    """Return only files approved by the bound review resolver."""

    resolver: ReviewFileResolver
    decision_store: ReviewDecisionStore | None

    def do_GET(self) -> None:
        path = self.resolver.resolve(self.path)
        if path is None:
            self.send_error(404)
            return
        try:
            content = path.read_bytes()
        except OSError as error:
            self.send_error(500, str(error))
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix == ".glb":
            content_type = "model/gltf-binary"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        if self.path != "/api/review-decision" or self.decision_store is None:
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 4096:
                raise ValueError("review decision has an invalid size")
            request = json.loads(self.rfile.read(length))
            decision = request.get("decision") if isinstance(request, dict) else None
            response = self.decision_store.decide(decision)
        except (OSError, ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})
            return
        self._send_json(200, response)

    def _send_json(self, status: int, value: dict) -> None:
        content = json.dumps(value).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, _format: str, *_args) -> None:
        return


class UnitReviewServer:
    """Own the short-lived loopback server used for one visual decision."""

    def __init__(
        self,
        viewer_root: Path,
        model_path: Path,
        port: int = 0,
        review_data_path: Path | None = None,
    ) -> None:
        resolver = ReviewFileResolver(viewer_root, model_path, review_data_path)
        decision_store = (
            ReviewDecisionStore(review_data_path) if review_data_path else None
        )
        handler: Type[ReviewRequestHandler] = type(
            "BoundReviewRequestHandler",
            (ReviewRequestHandler,),
            {"resolver": resolver, "decision_store": decision_store},
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.httpd.server_port}/"

    def open_browser(self) -> None:
        webbrowser.open(self.url)

    def serve(self) -> None:
        self.httpd.serve_forever()

    def close(self) -> None:
        self.httpd.server_close()
