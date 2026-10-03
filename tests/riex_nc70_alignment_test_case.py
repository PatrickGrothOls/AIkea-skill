"""Scope: Share exact source-CAD axis assertions across Riex alignment tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import unittest
from types import SimpleNamespace

import cadquery as cq

from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class PartFixture:
    dimensions_mm: tuple[tuple[str, float], ...]
    part_id: str
    local_size_mm: tuple
    local_to_parent: Any
    inside_face: str
    role: str = "panel"
    outline_mm: tuple = ()


class AssemblyFixture:
    width_mm = 1000.0
    door_width_mm = 998.0

    assembly_id = "alignment_01"

    @property
    def parts(self):
        return tuple(self.part(name) for name in ("left_side", "right_side", "door_panel"))

    def part(self, part_id: str) -> PartFixture:
        frames = {
            "left_side": ((0, 0, 0), ((0, 1, 0), (0, 0, 1), (1, 0, 0))),
            "right_side": ((1000, 582, 0), ((0, -1, 0), (0, 0, 1), (-1, 0, 0))),
            "door_panel": ((1, 0, 0), ((1, 0, 0), (0, 0, 1), (0, -1, 0))),
        }
        origin, axes = frames[part_id]
        point = SimpleNamespace(**dict(zip(("x_mm", "y_mm", "z_mm"), origin)))
        directions = tuple(SimpleNamespace(x=x, y=y, z=z) for x, y, z in axes)
        basis = SimpleNamespace(**dict(zip(("local_x_in_parent", "local_y_in_parent", "local_z_in_parent"), directions)))
        door = part_id == "door_panel"
        return PartFixture((("thickness", 18.0),), part_id,
                           (998 if door else 582, 1000, 18),
                           SimpleNamespace(origin_in_parent=point, axis_basis=basis), "<Z" if door else ">Z")


class RiexNc70AlignmentTestCase(unittest.TestCase):
    """Provide the approved cabinet frame and exact axis comparisons."""

    HINGE_CENTER_Z_MM = 500.0

    def setUp(self) -> None:
        self.assembly = AssemblyFixture()
        self.profile = RiexNc70HingeProfile()
        self.placement = RiexNc70HardwarePlacement()

    def global_point(
        self,
        location: Any,
        x_mm: float,
        y_mm: float,
        z_mm: float,
    ) -> tuple[float, float, float]:
        matrix = cq.Matrix(location.wrapped.Transformation())
        return cq.Vector(x_mm, y_mm, z_mm).transform(matrix).toTuple()

    def sort_axes(
        self,
        axes: tuple[tuple[float, float, float], ...],
    ) -> tuple[tuple[float, float, float], ...]:
        return tuple(sorted(axes, key=lambda item: (item[0], item[1], item[2])))

    def assert_axes_match(
        self,
        source_axes: tuple[tuple[float, float, float], ...],
        machining_axes: tuple[tuple[float, float, float], ...],
    ) -> None:
        for source_axis, machining_axis in zip(source_axes, machining_axes, strict=True):
            for actual_mm, expected_mm in zip(source_axis, machining_axis, strict=True):
                self.assertAlmostEqual(actual_mm, expected_mm, places=6)


__all__ = ["RiexNc70AlignmentTestCase"]
