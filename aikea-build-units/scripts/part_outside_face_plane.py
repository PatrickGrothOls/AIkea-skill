"""Scope: Resolve one generated sheet part's outside face in assembly space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cadquery as cq

from part_construction_error import PartConstructionError


@dataclass(frozen=True)
class OutsideFacePlane:
    """Carry a point inside the outside face and its outward normal."""

    center: cq.Vector
    normal: cq.Vector


class PartOutsideFacePlaneResolver:
    """Transform the canonical local outside face into assembly coordinates."""

    def resolve(self, part: Any, location: cq.Location) -> OutsideFacePlane:
        if part.inside_face not in {"<Z", ">Z"}:
            raise PartConstructionError(
                f"{part.part_id} does not define a supported inside face"
            )
        size_x_mm, size_y_mm, thickness_mm = (
            float(value) for value in part.local_size_mm
        )
        outside_z_mm = thickness_mm if part.inside_face == "<Z" else 0.0
        local_normal_z = 1.0 if part.inside_face == "<Z" else -1.0
        local_center = cq.Vector(size_x_mm / 2.0, size_y_mm / 2.0, outside_z_mm)
        local_tip = local_center + cq.Vector(0.0, 0.0, local_normal_z)
        center = self._locate_vector(local_center, location)
        tip = self._locate_vector(local_tip, location)
        return OutsideFacePlane(center, (tip - center).normalized())

    def _locate_vector(self, vector: cq.Vector, location: cq.Location) -> cq.Vector:
        return cq.Vertex.makeVertex(vector.x, vector.y, vector.z).located(location).Center()


__all__ = ["OutsideFacePlane", "PartOutsideFacePlaneResolver"]
