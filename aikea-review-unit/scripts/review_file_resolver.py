"""Scope: Resolve canonical local review paths to bundled static viewer files."""

from __future__ import annotations

from pathlib import Path


class ReviewFileResolver:
    """Keep static viewer lookups inside the bundled viewer root."""

    def __init__(self, viewer_root: Path) -> None:
        self.viewer_root = viewer_root.resolve()

    def resolve(self, path: str) -> Path | None:
        if path in ("/", "/index.html"):
            return self._existing(self.viewer_root / "index.html")
        candidate = (self.viewer_root / path.lstrip("/")).resolve()
        if not candidate.is_relative_to(self.viewer_root):
            return None
        return self._existing(candidate)

    def _existing(self, path: Path) -> Path | None:
        return path if path.is_file() else None
