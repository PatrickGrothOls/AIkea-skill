"""Scope: Rebuild the authoritative closed-tree GLB digest for approval checks."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from assembly_tree_review_geometry import AssemblyTreeReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from glb_artifact_snapshot import GlbArtifactSnapshot


class FabricationClosedAssemblyModel:
    """Render the current physical tree through the canonical review exporter."""

    def __init__(self) -> None:
        self.geometry = AssemblyTreeReviewGeometry()
        self.exporter = CadQueryGlbExporter()

    def expected_sha256(self, visits: tuple[Any, ...]) -> str:
        with TemporaryDirectory(prefix="aikea-closed-review-") as directory:
            path = Path(directory) / "full_wardrobe_review.glb"
            self.write(visits, path)
            return GlbArtifactSnapshot.load(path).sha256

    def write(self, visits: tuple[Any, ...], path: Path) -> None:
        parts = self.geometry.build(visits, {})
        self.exporter.export("full_wardrobe", parts, path)


__all__ = ["FabricationClosedAssemblyModel"]
