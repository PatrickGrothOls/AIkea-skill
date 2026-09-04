"""Scope: Verify installed KA 4532 fixing axes through the exact spacer."""

from __future__ import annotations

from typing import Any

from hettich_ka_4532_fixed_member_hole_pattern import (
    HETTICH_KA_4532_500_FIXED_MEMBER_HOLES,
)
from hettich_ka_4532_installed_runner_checker import (
    HettichKa4532InstalledRunnerChecker,
    HettichKa4532InstalledRunnerDatums,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952
from source_normalized_frame import SourceNormalizedFrame


class HettichKa4532SpacerInstalledFixingChecker:
    """Bind each exact rail bore to an inward spacer path and cabinet datum."""

    _TOLERANCE_MM = 1e-5
    _ENVELOPE_TOLERANCE_MM = 0.01

    def __init__(self) -> None:
        self.runners = HettichKa4532InstalledRunnerChecker()

    def axis_height(
        self,
        drawer_id: str,
        parts: dict[str, Any],
        step_set: Any,
    ) -> float | None:
        if not {
            f"{drawer_id}_spacer_left",
            f"{drawer_id}_spacer_right",
        } <= parts.keys():
            return None
        datums = self.runners.check(drawer_id, parts, step_set)
        if datums is None:
            return None
        heights: list[float] = []
        for side in ("left", "right"):
            side_heights = self._side_heights(
                side, drawer_id, parts, step_set, datums
            )
            if side_heights is None:
                return None
            heights.extend(side_heights)
        if max(heights) - min(heights) > self._TOLERANCE_MM:
            return None
        installed_height_mm = sum(heights) / len(heights)
        if (
            abs(installed_height_mm - datums.drawer_axis_height_mm)
            > self._TOLERANCE_MM
        ):
            return None
        return round(installed_height_mm, 6)

    def _side_heights(
        self,
        side: str,
        drawer_id: str,
        parts: dict[str, Any],
        step_set: Any,
        datums: HettichKa4532InstalledRunnerDatums,
    ) -> tuple[float, ...] | None:
        pattern = HETTICH_KA_4532_500_FIXED_MEMBER_HOLES
        profile = HETTICH_KA_4532_500_WITH_13952
        runner_source = getattr(step_set, f"runner_{side}").fixed_member
        spacer_source = step_set.spacer_solid
        runner_frame = SourceNormalizedFrame(
            parts[f"{drawer_id}_runner_{side}_fixed"], runner_source
        )
        spacer_frame = SourceNormalizedFrame(
            parts[f"{drawer_id}_spacer_{side}"], spacer_source
        )
        runner_bounds = runner_source.BoundingBox()
        spacer_bounds = spacer_source.BoundingBox()
        direction = 1.0 if side == "left" else -1.0
        runner_interface_x_mm = (
            runner_bounds.xmin if side == "left" else runner_bounds.xmax
        )
        runner_body_x_mm = (
            runner_bounds.xmax if side == "left" else runner_bounds.xmin
        )
        cabinet_inside_x_mm = datums.inside_x(side)
        heights = []
        for index, cabinet_depth_mm in enumerate(pattern.cabinet_depth_axes_mm):
            runner_native = (
                runner_interface_x_mm,
                pattern.fixed_member_native_depth_axes_mm[index],
                pattern.fixed_member_native_height_mm,
            )
            runner_body_native = (
                runner_body_x_mm,
                runner_native[1],
                runner_native[2],
            )
            spacer_native = (
                spacer_bounds.xmax,
                cabinet_depth_mm - profile.spacer_front_from_cabinet_front_mm,
                profile.runner_center_from_drawer_bottom_mm
                - profile.spacer_bottom_from_drawer_bottom_mm,
            )
            cabinet_native = (
                spacer_bounds.xmin,
                spacer_native[1],
                spacer_native[2],
            )
            runner_point = runner_frame.point(runner_native)
            spacer_point = spacer_frame.point(spacer_native)
            cabinet_point = spacer_frame.point(cabinet_native)
            if not self._axis_matches(
                runner_point,
                spacer_point,
                cabinet_point,
                runner_frame.unit_direction(runner_native, runner_body_native),
                spacer_frame.unit_direction(cabinet_native, spacer_native),
                cabinet_inside_x_mm,
                datums.cabinet_front_mm + cabinet_depth_mm,
                direction,
            ):
                return None
            heights.append(runner_point[2])
        return tuple(heights)

    def _axis_matches(
        self,
        runner_point: tuple[float, ...],
        spacer_point: tuple[float, ...],
        cabinet_point: tuple[float, ...],
        runner_direction: tuple[float, ...],
        spacer_direction: tuple[float, ...],
        cabinet_inside_x_mm: float,
        expected_depth_mm: float,
        direction: float,
    ) -> bool:
        expected_interface_x_mm = cabinet_inside_x_mm + direction * (
            HETTICH_KA_4532_500_WITH_13952.spacer_width_per_side_mm
        )
        return (
            self._same(runner_point, spacer_point, self._TOLERANCE_MM)
            and self._same(runner_direction, spacer_direction, self._TOLERANCE_MM)
            and self._same(cabinet_point[1:], runner_point[1:], self._TOLERANCE_MM)
            and abs(cabinet_point[0] - cabinet_inside_x_mm)
            <= self._ENVELOPE_TOLERANCE_MM
            and abs(runner_point[0] - expected_interface_x_mm)
            <= self._ENVELOPE_TOLERANCE_MM
            and abs(runner_point[1] - expected_depth_mm) <= self._TOLERANCE_MM
        )

    def _same(
        self,
        left: tuple[float, ...],
        right: tuple[float, ...],
        tolerance_mm: float,
    ) -> bool:
        return all(
            abs(left_value - right_value) <= tolerance_mm
            for left_value, right_value in zip(left, right)
        )


__all__ = ["HettichKa4532SpacerInstalledFixingChecker"]
