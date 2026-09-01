"""Scope: Compare exported STEP and DXF files with authoritative built parts."""

from __future__ import annotations

from math import isclose
from pathlib import Path

import cadquery as cq

from fabrication_readiness_report import FabricationReadinessCheck
from fabrication_tree_evidence import FabricationPartEvidence


class FabricationPartArtifactChecker:
    """Reject unreadable, placeholder, stale, or dimensionally wrong part files."""

    _ABSOLUTE_TOLERANCE_MM = 1e-4
    _MINIMUM_VOLUME_MM3 = 1e-6

    def check(
        self,
        project_root: Path,
        parts: tuple[FabricationPartEvidence, ...],
    ) -> FabricationReadinessCheck:
        problems = tuple(
            problem
            for part in parts
            for problem in self._part_problems(project_root, part)
        )
        return FabricationReadinessCheck(
            "pack.part_step_and_drawings",
            not problems,
            problems,
        )

    def _part_problems(
        self,
        root: Path,
        evidence: FabricationPartEvidence,
    ) -> tuple[str, ...]:
        base = root / "manufacturing/parts" / self._slug(evidence.path)
        checks = (
            (base.with_suffix(".step"), self._step_matches),
            (base.with_suffix(".dxf"), self._dxf_matches),
        )
        return tuple(
            f"{path.relative_to(root)}: {problem}"
            for path, validator in checks
            for problem in validator(path, evidence)
        )

    def _step_matches(
        self,
        path: Path,
        evidence: FabricationPartEvidence,
    ) -> tuple[str, ...]:
        try:
            exported = cq.importers.importStep(str(path)).val()
        except (OSError, RuntimeError, ValueError):
            return ("unreadable STEP solid",)
        source = evidence.part.solid.val()
        if not exported.isValid() or exported.Volume() <= self._MINIMUM_VOLUME_MM3:
            return ("invalid STEP solid",)
        tolerance = max(
            self._MINIMUM_VOLUME_MM3,
            source.Volume() * 1e-9,
        )
        difference = source.cut(exported).Volume() + exported.cut(source).Volume()
        return () if difference <= tolerance else ("STEP differs from built geometry",)

    def _dxf_matches(
        self,
        path: Path,
        evidence: FabricationPartEvidence,
    ) -> tuple[str, ...]:
        try:
            shapes = tuple(cq.importers.importDXF(str(path)).vals())
        except (OSError, RuntimeError, ValueError):
            return ("unreadable DXF drawing",)
        faces = tuple(shape for shape in shapes if shape.ShapeType() == "Face")
        if not faces:
            return ("DXF has no closed drawing face",)
        drawing_bounds = cq.Compound.makeCompound(faces).BoundingBox()
        source_bounds = evidence.part.solid.val().BoundingBox()
        matches = all(
            isclose(
                actual,
                expected,
                rel_tol=0.0,
                abs_tol=self._ABSOLUTE_TOLERANCE_MM,
            )
            for actual, expected in (
                (drawing_bounds.xlen, source_bounds.xlen),
                (drawing_bounds.ylen, source_bounds.ylen),
            )
        )
        return () if matches else ("DXF footprint differs from built geometry",)

    def _slug(self, path: str) -> str:
        return path.replace("/", "__")


__all__ = ["FabricationPartArtifactChecker"]
