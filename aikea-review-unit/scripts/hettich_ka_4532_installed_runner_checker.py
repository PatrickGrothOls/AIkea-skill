"""Scope: Verify installed KA 4532 runner articulation and drawer datums."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952
from source_normalized_frame import SourceNormalizedFrame


@dataclass(frozen=True, slots=True)
class HettichKa4532InstalledRunnerDatums:
    """Carry cabinet and drawer datums after their relationship is verified."""

    cabinet_front_mm: float
    drawer_axis_height_mm: float
    cabinet_inside_x_mm: tuple[float, float]

    def inside_x(self, side: str) -> float:
        return self.cabinet_inside_x_mm[0 if side == "left" else 1]


class HettichKa4532InstalledRunnerChecker:
    """Bind exact fixed and moving members to the wooden drawer and carcass."""

    _TOLERANCE_MM = 1e-5
    _ENVELOPE_TOLERANCE_MM = 0.01

    def check(
        self,
        drawer_id: str,
        parts: dict[str, Any],
        step_set: Any,
        host=None,
    ) -> HettichKa4532InstalledRunnerDatums | None:
        host_names = tuple(host.part(side).part_id for side in ("left", "right")) if host is not None else ("left_side", "right_side")
        required = {
            *host_names,
            *(
                f"{drawer_id}__{part}"
                for part in ("left_side", "right_side", "front", "back", "bottom")
            ),
            *(f"{drawer_id}_runner_{side}_fixed" for side in ("left", "right")),
            *(
                f"{drawer_id}__{drawer_id}_runner_{side}_moving"
                for side in ("left", "right")
            ),
        }
        if not required <= parts.keys():
            return None
        if host is not None and not self._host_matches(host, drawer_id, parts):
            return None
        cabinet_front_mm = host.spec.front_mm if host is not None else self._matching_average(
            tuple(
                float(parts[name].placed_shape().BoundingBox().ymin)
                for name in host_names
            )
        )
        drawer_bottom_mm = self._matching_average(
            tuple(
                float(parts[f"{drawer_id}__{part}"].placed_shape().BoundingBox().zmin)
                for part in ("left_side", "right_side", "front", "back")
            )
        )
        if cabinet_front_mm is None or drawer_bottom_mm is None:
            return None
        profile = HETTICH_KA_4532_500_WITH_13952
        drawer_axis_height_mm = (
            drawer_bottom_mm + profile.runner_center_from_drawer_bottom_mm
        )
        moving_heights = tuple(
            self._mid_height(
                parts[f"{drawer_id}__{drawer_id}_runner_{side}_moving"]
            )
            for side in ("left", "right")
        )
        if (
            max((*moving_heights, drawer_axis_height_mm))
            - min(*moving_heights, drawer_axis_height_mm)
            > self._ENVELOPE_TOLERANCE_MM
        ):
            return None
        drawer_front_bounds = parts[
            f"{drawer_id}__front"
        ].placed_shape().BoundingBox()
        drawer_front_mm = float(drawer_front_bounds.ymin)
        drawer_box_front_mm = float(drawer_front_bounds.ymax)
        if self._matching_average(
            tuple(
                float(
                    parts[f"{drawer_id}__{part}"]
                    .placed_shape()
                    .BoundingBox()
                    .ymin
                )
                for part in ("left_side", "right_side", "bottom")
            )
            + (drawer_box_front_mm,)
        ) is None:
            return None
        inside_x_mm = tuple(
            self._cabinet_inside_x(side, parts[name]) for side, name in zip(("left", "right"), host_names)
        )
        for side, cabinet_inside_x_mm in zip(("left", "right"), inside_x_mm):
            direction = 1.0 if side == "left" else -1.0
            drawer_bounds = parts[
                f"{drawer_id}__{side}_side"
            ].placed_shape().BoundingBox()
            drawer_outer_x_mm = float(
                drawer_bounds.xmin if side == "left" else drawer_bounds.xmax
            )
            fixed_source = getattr(step_set, f"runner_{side}").fixed_member
            moving_source = getattr(step_set, f"runner_{side}").moving_member
            fixed_frame = SourceNormalizedFrame(
                parts[f"{drawer_id}_runner_{side}_fixed"], fixed_source
            )
            moving_frame = SourceNormalizedFrame(
                parts[f"{drawer_id}__{drawer_id}_runner_{side}_moving"],
                moving_source,
            )
            if (
                abs(
                    drawer_outer_x_mm
                    - cabinet_inside_x_mm
                    - direction * profile.hardware_width_per_side_mm
                )
                > self._ENVELOPE_TOLERANCE_MM
                or not fixed_frame.translated_matches(
                    moving_frame,
                    (0.0, drawer_front_mm - cabinet_front_mm, 0.0),
                    self._TOLERANCE_MM,
                )
            ):
                return None
        return HettichKa4532InstalledRunnerDatums(
            cabinet_front_mm,
            drawer_axis_height_mm,
            inside_x_mm,
        )

    def _host_matches(self, host, drawer_id, parts):
        names = tuple(host.part(side).part_id for side in ("left", "right"))
        children = tuple(f"{drawer_id}__{name}" for name in ("left_side", "right_side", "front", "back", "bottom"))
        for side, name in zip(("left", "right"), names):
            bounds = parts[name].placed_shape().BoundingBox()
            inside = bounds.xmax if side == "left" else bounds.xmin
            if abs(inside-host.inside_x(side)) > self._ENVELOPE_TOLERANCE_MM:
                return False
        space = host.spec
        intervals = (("x", host.inside_x("left"), host.inside_x("right")),
                     ("y", space.front_mm, space.front_mm+space.inside_depth_mm),
                     ("z", space.bottom_mm, space.top_mm))
        return all(getattr(bounds, axis+"min") >= lower-self._ENVELOPE_TOLERANCE_MM and
                   getattr(bounds, axis+"max") <= upper+self._ENVELOPE_TOLERANCE_MM
                   for name in children for bounds in (parts[name].placed_shape().BoundingBox(),)
                   for axis, lower, upper in intervals)

    def _cabinet_inside_x(self, side: str, part: Any) -> float:
        bounds = part.placed_shape().BoundingBox()
        return float(bounds.xmax if side == "left" else bounds.xmin)

    def _matching_average(self, values: tuple[float, ...]) -> float | None:
        if max(values) - min(values) > self._ENVELOPE_TOLERANCE_MM:
            return None
        return sum(values) / len(values)

    def _mid_height(self, part: Any) -> float:
        bounds = part.placed_shape().BoundingBox()
        return (float(bounds.zmin) + float(bounds.zmax)) / 2.0


__all__ = [
    "HettichKa4532InstalledRunnerChecker",
    "HettichKa4532InstalledRunnerDatums",
]
