"""Scope: Load and normalize the packaged Cabineo cutter solids."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import cadquery as cq

from cabineo_profile import CabineoProfile


@dataclass(frozen=True)
class CabineoCutterGeometry:
    """Preserve the proven STEP normalization and entry-pin alignment."""

    asset_root: Path

    @classmethod
    def packaged(cls) -> "CabineoCutterGeometry":
        return cls(Path(__file__).resolve().parents[1] / "assets" / "cabineo")

    @lru_cache(maxsize=4)
    def load(self, profile: CabineoProfile) -> cq.Shape:
        connector = cq.importers.importStep(
            str(self.asset_root / profile.cutter_asset_filename)
        ).val()
        connector = connector.rotate((0, 0, 0), (0, 0, 1), -90)
        bbox = connector.BoundingBox()
        normalized = connector.translate(
            (
                -(bbox.xmin + bbox.xlen / 2.0),
                -bbox.ymin,
                profile.pocket_depth_mm - bbox.zmax,
            )
        )
        aligned = self._align_entry_pin(normalized, profile)
        return self._extend_floor(aligned, profile.extra_floor_mm)

    def _align_entry_pin(
        self, shape: cq.Shape, profile: CabineoProfile
    ) -> cq.Shape:
        y_offset = self._working_entry_pin_ymax(profile) - self._entry_pin_ymax(shape)
        return shape.translate((0.0, y_offset, 0.0))

    @lru_cache(maxsize=4)
    def _working_entry_pin_ymax(self, profile: CabineoProfile) -> float:
        path = self.asset_root / profile.alignment_asset_filename
        raw = cq.importers.importStep(str(path)).val()
        bbox = raw.BoundingBox()
        normalized = raw.translate(
            (
                -(bbox.xmin + bbox.xlen / 2.0),
                -bbox.ymin,
                profile.pocket_depth_mm - bbox.zmax,
            )
        )
        return self._entry_pin_ymax(
            self._extend_floor(normalized, profile.extra_floor_mm)
        )

    def _entry_pin_ymax(self, shape: cq.Shape) -> float:
        candidates: list[tuple[float, float]] = []
        for face in shape.Faces():
            if face.geomType() != "CYLINDER":
                continue
            bbox = face.BoundingBox()
            if (
                bbox.ymin <= 0.75
                and bbox.ylen >= 6.0
                and bbox.xlen <= 10.0
                and bbox.zlen <= 10.0
            ):
                candidates.append((bbox.ymin, bbox.ymax))
        if not candidates:
            raise RuntimeError("Could not find Cabineo entry pin cylinder in cutter.")
        return min(candidates, key=lambda item: item[0])[1]

    def _extend_floor(self, shape: cq.Shape, extra_floor_mm: float) -> cq.Shape:
        extension = (
            cq.Workplane("XY")
            .newObject([shape])
            .faces(">Z")
            .wires()
            .toPending()
            .extrude(extra_floor_mm)
            .val()
        )
        return shape.fuse(extension)


__all__ = ["CabineoCutterGeometry"]
