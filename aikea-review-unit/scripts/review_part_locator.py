"""Scope: Apply review-only poses to canonical assembly part locations."""

from __future__ import annotations

from math import cos, radians, sin
from typing import Any

import cadquery as cq

from assembly_part_locator import AssemblyPartLocator


class ReviewPartLocator:
    """Keep visual presentation transforms outside physical construction."""

    _OPEN_DOOR_ANGLE_DEGREES = -90.0

    def __init__(self) -> None:
        self.assembly_locator = AssemblyPartLocator()

    def locate(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        if part.part_id != "door_panel":
            return self.assembly_locator.locate(part, assembly, base_height_mm)
        angle = radians(self._OPEN_DOOR_ANGLE_DEGREES)
        left_gap_mm = (
            float(assembly.width_mm) - float(assembly.door_width_mm)
        ) / 2.0
        return cq.Location(
            cq.Plane(
                origin=(left_gap_mm, 0.0, float(assembly.door_bottom_mm)),
                xDir=(cos(angle), sin(angle), 0.0),
                normal=(sin(angle), -cos(angle), 0.0),
            )
        )


__all__ = ["ReviewPartLocator"]
