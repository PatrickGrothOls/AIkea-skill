"""Scope: Create paired local cuts for one equal-thickness panel miter."""

from __future__ import annotations

from math import isclose
from typing import Any

import cadquery as cq

from miter_edge_mate import MiterEdgeMate
from part_construction_error import PartConstructionError
from part_cut import PartCut
from part_outside_face_plane import PartOutsideFacePlaneResolver


class EqualThicknessMiterJoint:
    """Cut both participants from one shared assembly-space bisecting plane."""

    def __init__(self) -> None:
        self.outside_face_plane = PartOutsideFacePlaneResolver()

    def build(
        self,
        joint: Any,
        part_a: Any,
        part_b: Any,
        location_a: cq.Location,
        location_b: cq.Location,
    ) -> tuple[PartCut, PartCut]:
        self._validate_equal_thickness(part_a, part_b)
        plane_a = self.outside_face_plane.resolve(part_a, location_a)
        plane_b = self.outside_face_plane.resolve(part_b, location_b)
        mate = MiterEdgeMate.from_planes(
            plane_a.center,
            plane_a.normal,
            plane_b.center,
            plane_b.normal,
        )
        return (
            PartCut(
                joint.joint_id,
                part_a.part_id,
                1,
                mate.cutter_for_a(),
                location_a.inverse,
            ),
            PartCut(
                joint.joint_id,
                part_b.part_id,
                1,
                mate.cutter_for_b(),
                location_b.inverse,
            ),
        )

    def _validate_equal_thickness(self, part_a: Any, part_b: Any) -> None:
        thickness_a_mm = float(part_a.local_size_mm[2])
        thickness_b_mm = float(part_b.local_size_mm[2])
        if not isclose(thickness_a_mm, thickness_b_mm, abs_tol=1e-6):
            raise PartConstructionError(
                f"{part_a.part_id} and {part_b.part_id} require equal thickness for a miter"
            )


__all__ = ["EqualThicknessMiterJoint"]
