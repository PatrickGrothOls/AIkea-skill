"""Scope: Locate one panel's canonical local frame inside its assembly."""

from __future__ import annotations

from math import hypot
from typing import Any

import cadquery as cq

from part_construction_error import PartConstructionError


class AssemblyPartLocator:
    """Calculate explicit local-to-assembly transforms for generated panel parts."""

    def __init__(self) -> None:
        self._part_locators = {
            "left_side": self._left_side,
            "right_side": self._right_side,
            "back_panel": self._back_panel,
            "door_panel": self._door_panel,
        }
        self._role_locators = {
            "shelf_panel": self._shelf_panel,
            "top_panel": self._top_panel,
        }

    def locate(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        locator = self._part_locators.get(part.part_id)
        locator = locator or self._role_locators.get(part.role)
        if locator is None:
            raise PartConstructionError(
                f"no assembly placement exists for {part.part_id}"
            )
        return locator(part, assembly, base_height_mm)

    def _left_side(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        return self._location(
            (0.0, 0.0, base_height_mm),
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
        )

    def _right_side(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        return self._location(
            (float(assembly.width_mm), float(assembly.inside_depth_mm), base_height_mm),
            (0.0, -1.0, 0.0),
            (-1.0, 0.0, 0.0),
        )

    def _back_panel(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        return self._location(
            (0.0, float(assembly.depth_mm), base_height_mm),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        )

    def _door_panel(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        left_gap_mm = (float(assembly.width_mm) - float(assembly.door_width_mm)) / 2.0
        return self._location(
            (left_gap_mm, 0.0, float(assembly.door_bottom_mm)),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        )

    def _shelf_panel(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        dimensions = self._dimensions(part)
        return self._location(
            (
                dimensions["assembly_x"],
                dimensions["assembly_y"],
                base_height_mm + dimensions["bottom_height"],
            ),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

    def _top_panel(self, part: Any, assembly: Any, base_height_mm: float) -> cq.Location:
        dimensions = self._dimensions(part)
        run_mm = dimensions["end_x"] - dimensions["start_x"]
        rise_mm = dimensions["end_height"] - dimensions["start_height"]
        length_mm = hypot(run_mm, rise_mm)
        tangent = (run_mm / length_mm, 0.0, rise_mm / length_mm)
        outside_normal = (-rise_mm / length_mm, 0.0, run_mm / length_mm)
        thickness_mm = dimensions["thickness"]
        outside_start = (
            dimensions["start_x"],
            0.0,
            base_height_mm + dimensions["start_height"],
        )
        inside_start = tuple(
            coordinate - normal * thickness_mm
            for coordinate, normal in zip(outside_start, outside_normal)
        )
        return self._location(inside_start, tangent, outside_normal)

    def _location(
        self,
        origin: tuple[float, float, float],
        local_x: tuple[float, float, float],
        local_z: tuple[float, float, float],
    ) -> cq.Location:
        return cq.Location(cq.Plane(origin=origin, xDir=local_x, normal=local_z))

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["AssemblyPartLocator"]
