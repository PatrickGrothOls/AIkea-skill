"""Scope: Exercise one loopback review server with authentic GLB artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import cadquery as cq

from cadquery_glb_exporter import CadQueryGlbExporter
from unit_mockup import MockupPart
from unit_review_server import UnitReviewServer


class ReviewServerTestSupport:
    """Create viewer files, write GLBs, and make bounded HTTP requests."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.viewer = root / "viewer"
        self.viewer.mkdir()
        (self.viewer / "index.html").write_text("review", encoding="utf-8")

    def write_model(self, name: str = "model.glb", size: float = 10.0) -> Path:
        path = self.root / "assemblies" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        CadQueryGlbExporter().export(
            "wardrobe_01",
            (
                MockupPart(
                    "panel",
                    cq.Workplane("XY").box(size, 10.0, 10.0),
                    cq.Location(),
                    (0.8, 0.7, 0.6, 1.0),
                ),
            ),
            path,
        )
        return path

    def write_json(self, relative: str, value: dict) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def start(self, model: Path, review: Path) -> UnitReviewServer:
        return UnitReviewServer(self.viewer, model, 0, review)

    def request(
        self,
        server: UnitReviewServer,
        path: str,
        method: str = "GET",
        body: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, bytes]:
        request_thread = Thread(target=server.httpd.handle_request)
        request_thread.start()
        request = Request(
            f"{server.url}{path}",
            data=(json.dumps(body).encode("utf-8") if body is not None else None),
            headers=headers or {},
            method=method,
        )
        try:
            with urlopen(request, timeout=2) as response:
                result = response.status, response.read()
        except HTTPError as error:
            result = error.code, error.read()
        request_thread.join(timeout=2)
        if request_thread.is_alive():
            raise AssertionError("review request did not finish")
        return result


__all__ = ["ReviewServerTestSupport"]
