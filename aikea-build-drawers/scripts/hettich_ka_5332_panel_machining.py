"""Scope: Machine exact KA 5332 fixings in cabinet and drawer side panels."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import cadquery as cq

from hettich_ka_5332_runner_profile import (
    HETTICH_KA_5332_500,
    HettichKa5332RunnerProfile,
)


class HettichKa5332PanelMachining:
    """Cut the official 500 mm fixing pattern in each participating sheet."""

    def __init__(
        self,
        profile: HettichKa5332RunnerProfile = HETTICH_KA_5332_500,
    ) -> None:
        self.profile = profile

    def cabinet_parts(
        self,
        parts: tuple[Any, ...],
        row_heights_mm: tuple[float, ...],
    ) -> tuple[Any, ...]:
        return tuple(
            replace(part, solid=self._cabinet_side(part, row_heights_mm))
            if part.spec.part_id in {"left_side", "right_side"}
            else part
            for part in parts
        )

    def drawer_box(self, box: Any) -> Any:
        return replace(
            box,
            parts=tuple(
                replace(part, solid=self._drawer_side(part))
                if part.spec.part_id in {"left_side", "right_side"}
                else part
                for part in box.parts
            ),
        )

    def _cabinet_side(self, part: Any, rows_mm: tuple[float, ...]) -> Any:
        depth_mm, _, thickness_mm = map(float, part.spec.local_size_mm)
        front_positions_mm = self.profile.cabinet_fixing_positions_from_front_mm
        x_positions_mm = (
            front_positions_mm
            if part.spec.part_id == "left_side"
            else tuple(depth_mm - value for value in front_positions_mm)
        )
        points = tuple((x_mm, row_mm) for row_mm in rows_mm for x_mm in x_positions_mm)
        cutter = self._inside_face_cutter(
            points,
            thickness_mm,
            self.profile.cabinet_hole_diameter_mm,
            self.profile.cabinet_hole_depth_mm,
        )
        return part.solid.cut(cutter)

    def _drawer_side(self, part: Any) -> Any:
        length_mm, _, thickness_mm = map(float, part.spec.local_size_mm)
        front_positions_mm = self.profile.drawer_fixing_positions_from_front_mm
        x_positions_mm = (
            tuple(length_mm - value for value in front_positions_mm)
            if part.spec.part_id == "left_side"
            else front_positions_mm
        )
        points = tuple(
            (x_mm, self.profile.runner_center_from_drawer_bottom_mm)
            for x_mm in x_positions_mm
        )
        cutter = self._inside_face_cutter(
            points,
            thickness_mm,
            self.profile.drawer_pilot_diameter_mm,
            self.profile.drawer_pilot_depth_mm,
        )
        return part.solid.cut(cutter)

    def _inside_face_cutter(
        self,
        points: tuple[tuple[float, float], ...],
        thickness_mm: float,
        diameter_mm: float,
        depth_mm: float,
    ) -> cq.Workplane:
        return (
            cq.Workplane("XY", origin=(0.0, 0.0, thickness_mm - depth_mm))
            .pushPoints(points)
            .circle(diameter_mm / 2.0)
            .extrude(depth_mm)
        )


__all__ = ["HettichKa5332PanelMachining"]
