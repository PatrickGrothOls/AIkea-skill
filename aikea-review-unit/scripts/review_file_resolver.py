"""Scope: Resolve local review URLs to bundled viewer files or one chosen GLB."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import unquote, urlsplit


class ReviewFileResolver:
    """Keep the temporary review server inside two explicit read roots."""

    def __init__(self, viewer_root: Path, model_path: Path) -> None:
        self.viewer_root = viewer_root.resolve()
        self.model_path = model_path.resolve()

    def resolve(self, request_target: str) -> Path | None:
        path = unquote(urlsplit(request_target).path)
        if path in ("/", "/index.html"):
            return self._existing(self.viewer_root / "index.html")
        if path == "/model.glb":
            return self._existing(self.model_path)
        candidate = (self.viewer_root / path.lstrip("/")).resolve()
        if not candidate.is_relative_to(self.viewer_root):
            return None
        return self._existing(candidate)

    def _existing(self, path: Path) -> Path | None:
        return path if path.is_file() else None
