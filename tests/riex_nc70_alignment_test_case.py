"""Scope: Share exact source-CAD axis assertions across Riex alignment tests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import unittest

import cadquery as cq

from riex_nc70_hardware_placement import RiexNc70HardwarePlacement
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class PartFixture:
    dimensions_mm: tuple[tuple[str, float], ...]


class AssemblyFixture:
    width_mm = 1000.0
    door_width_mm = 998.0

    def part(self, part_id: str) -> PartFixture:
        if part_id not in {"left_side", "right_side"}:
            raise KeyError(part_id)
        return PartFixture((("thickness", 18.0),))


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
