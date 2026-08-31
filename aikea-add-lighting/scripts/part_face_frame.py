"""Scope: Resolve a named sheet face into an explicit local coordinate frame."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cadquery as cq


Vector3 = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class PartFaceFrame:
    """Describe one right-handed face plane in its owning part."""

    face: str
    origin_in_part_mm: Vector3
    local_x_in_part: Vector3
    local_y_in_part: Vector3
    local_z_in_part: Vector3
    width_mm: float
    height_mm: float
    material_depth_mm: float

    def location(self) -> cq.Location:
        return cq.Location(
            cq.Plane(
                origin=self.origin_in_part_mm,
                xDir=self.local_x_in_part,
                normal=self.local_z_in_part,
            )
        )

    def as_record(self) -> dict[str, object]:
        return {
            "face": self.face,
            "origin_in_part_mm": list(self.origin_in_part_mm),
            "local_x_in_part": list(self.local_x_in_part),
            "local_y_in_part": list(self.local_y_in_part),
            "local_z_in_part": list(self.local_z_in_part),
            "face_size_mm": [self.width_mm, self.height_mm],
            "material_depth_mm": self.material_depth_mm,
        }


class PartFaceFrameBuilder:
    """Build consistent coordinates for any canonical rectangular-sheet face."""

    def build(self, part: Any, face: str) -> PartFaceFrame:
        size_x, size_y, size_z = (float(value) for value in part.local_size_mm)
        frames = {
            ">X": ((size_x, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), size_y, size_z, size_x),
            "<X": ((0.0, size_y, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (-1.0, 0.0, 0.0), size_y, size_z, size_x),
            ">Y": ((size_x, size_y, 0.0), (-1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), size_x, size_z, size_y),
            "<Y": ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, -1.0, 0.0), size_x, size_z, size_y),
            ">Z": ((0.0, 0.0, size_z), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), size_x, size_y, size_z),
            "<Z": ((size_x, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, -1.0), size_x, size_y, size_z),
        }
        if face not in frames:
            raise ValueError(f"unsupported part face: {face}")
        origin, local_x, local_y, local_z, width, height, depth = frames[face]
        return PartFaceFrame(
            face,
            origin,
            local_x,
            local_y,
            local_z,
            width,
            height,
            depth,
        )


__all__ = ["PartFaceFrame", "PartFaceFrameBuilder", "Vector3"]
