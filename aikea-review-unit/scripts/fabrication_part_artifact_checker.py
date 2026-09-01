"""Scope: Compare exported STEP and DXF files with authoritative built parts."""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

from blank_sheet_builder import BlankSheetBuilder
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
        if len(faces) != 1:
            return ("DXF must contain one closed drawing face",)
        drawing_bounds = faces[0].BoundingBox()
        if drawing_bounds.zlen > self._ABSOLUTE_TOLERANCE_MM:
            return ("DXF drawing is not planar",)
        drawing = faces[0].moved(
            cq.Location(cq.Vector(0.0, 0.0, -drawing_bounds.zmin))
        )
        source = self._source_footprint(evidence)
        difference_area = source.cut(drawing).Area() + drawing.cut(source).Area()
        tolerance = max(
            self._ABSOLUTE_TOLERANCE_MM**2,
            source.Area() * 1e-9,
        )
        return (
            ()
            if difference_area <= tolerance
            else ("DXF footprint differs from built geometry",)
        )

    def _source_footprint(self, evidence: FabricationPartEvidence):
        spec = evidence.part.spec
        declared = getattr(spec, "outline_mm", ())
        outline = tuple(
            (float(point.x_mm), float(point.height_mm)) for point in declared
        )
        if not outline:
            width_mm, height_mm, _thickness_mm = spec.local_size_mm
            outline = BlankSheetBuilder.rectangle(
                float(width_mm),
                float(height_mm),
                1.0,
            ).outline_mm
        return BlankSheetBuilder(outline, 1.0).build().faces("<Z").val()

    def _slug(self, path: str) -> str:
        return path.replace("/", "__")


__all__ = ["FabricationPartArtifactChecker"]
