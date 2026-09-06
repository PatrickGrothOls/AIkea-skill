"""Scope: Serve one immutable GLB through the bundled local review viewer."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import mimetypes
from pathlib import Path
from typing import Type
from urllib.parse import unquote, urlsplit
import webbrowser

from review_decision_store import ReviewDecisionConflict
from review_file_resolver import ReviewFileResolver
from review_server_session import ReviewServerSession


class ReviewRequestHandler(BaseHTTPRequestHandler):
    """Return bound files and accept one protected same-origin decision."""

    resolver: ReviewFileResolver
    session: ReviewServerSession
    origin: str

    def do_GET(self) -> None:
        request_path = self._decoded_path()
        if request_path == "/model.glb":
            self._send_bytes(200, self.session.artifact.content, "model/gltf-binary")
            return
        if request_path == "/review-data.json" and self.session.store:
            try:
                self._send_json(200, self.session.review_data())
            except ReviewDecisionConflict as error:
                self._send_json(409, {"error": str(error)})
            return
        path = self.resolver.resolve(request_path)
        if path is None:
            self.send_error(404)
            return
        try:
            content = path.read_bytes()
        except OSError as error:
            self.send_error(500, str(error))
            return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self._send_bytes(200, content, content_type)

    def do_POST(self) -> None:
        if self._decoded_path() != "/api/review-decision" or not self.session.store:
            self.send_error(404)
            return
        content_type = self.headers.get("Content-Type", "").partition(";")[0].lower()
        if content_type != "application/json":
            self._send_json(415, {"error": "review decision must be JSON"})
            return
        if self.headers.get("Origin") != self.origin:
            self._send_json(403, {"error": "review decision origin is invalid"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 4096:
                raise ValueError("review decision has an invalid size")
            request = json.loads(self.rfile.read(length))
            decision = request.get("decision") if isinstance(request, dict) else None
            response = self.session.decide(
                decision,
                self.headers.get("X-AIkea-Review-Token"),
            )
        except PermissionError as error:
            self._send_json(403, {"error": str(error)})
            return
        except ReviewDecisionConflict as error:
            self._send_json(409, {"error": str(error)})
            return
        except (OSError, ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})
            return
        self._send_json(200, response)

    def _decoded_path(self) -> str:
        encoded_path = urlsplit(self.path).path
        return unquote(unquote(encoded_path))

    def _send_json(self, status: int, value: dict) -> None:
        self._send_bytes(
            status,
            json.dumps(value).encode("utf-8"),
            "application/json",
            no_store=True,
        )

    def _send_bytes(
        self,
        status: int,
        content: bytes,
        content_type: str,
        no_store: bool = False,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        if no_store:
            self.send_header("Cache-Control", "no-store")
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
        resolver = ReviewFileResolver(viewer_root)
        session = ReviewServerSession(model_path, review_data_path)
        handler: Type[ReviewRequestHandler] = type(
            "BoundReviewRequestHandler",
            (ReviewRequestHandler,),
            {"resolver": resolver, "session": session, "origin": ""},
        )
        self.httpd = ThreadingHTTPServer(("127.0.0.1", port), handler)
        handler.origin = f"http://127.0.0.1:{self.httpd.server_port}"

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.httpd.server_port}/"

    def open_browser(self) -> None:
        webbrowser.open(self.url)

    def serve(self) -> None:
        self.httpd.serve_forever()

    def close(self) -> None:
        self.httpd.server_close()


__all__ = ["UnitReviewServer"]
