"""Scope: Show the known fixed and drawer-following parts of runner movement."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart


class RunnerMovementPreviewGeometry:
    """Build a visibly simplified motion guide without imitating vendor internals."""

    _FRONT_NATIVE_Z_MM = 35.0
    _TRACK_WIDTH_MM = 5.0
    _TRACK_HEIGHT_MM = 6.0
    _FIXED_NATIVE_Y_MM = -31.0
    _FOLLOWER_NATIVE_Y_MM = -22.0
    _FIXED_COLOR = (0.23, 0.27, 0.31, 1.0)
    _FOLLOWER_COLOR = (0.72, 0.48, 0.20, 1.0)

    def __init__(self) -> None:
        self.frame_location = LocalToParentLocation()
        self.review_motion = DrawerReviewMotion()

    def build(
        self,
        built_cabinet: Any,
        runner: Any,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        if state is DrawerReviewState.REMOVED:
            return ()
        child = self._drawer_child(built_cabinet)
        runner_specs = {
            item.spec.hardware_id: item.spec
            for item in built_cabinet.purchased_hardware
        }
        child_frame = self.frame_location.build(child.spec.local_to_parent)
        local_motion = self.review_motion.location(
            state,
            child.assembly.spec.box.side_length_mm,
        )
        parent_motion = child_frame * local_motion * child_frame.inverse
        parts: list[MockupPart] = []
        for hand in ("left", "right"):
            runner_frame = self.frame_location.build(
                runner_specs[f"runner_{hand}"].local_to_parent
            )
            parts.extend(
                (
                    MockupPart(
                        f"review_only__runner_{hand}__fixed_path",
                        self._track(hand, runner.nominal_length_mm, fixed=True),
                        runner_frame,
                        self._FIXED_COLOR,
                    ),
                    MockupPart(
                        f"review_only__runner_{hand}__drawer_side_guide",
                        self._track(hand, runner.nominal_length_mm, fixed=False),
                        parent_motion * runner_frame,
                        self._FOLLOWER_COLOR,
                    ),
                )
            )
        return tuple(parts)

    def _track(self, hand: str, length_mm: float, fixed: bool) -> cq.Workplane:
        x_start = 0.0 if hand == "left" else -self._TRACK_WIDTH_MM
        y_start = (
            self._FIXED_NATIVE_Y_MM
            if fixed
            else self._FOLLOWER_NATIVE_Y_MM
        )
        z_start = self._FRONT_NATIVE_Z_MM - length_mm
        return (
            cq.Workplane("XY")
            .box(
                self._TRACK_WIDTH_MM,
                self._TRACK_HEIGHT_MM,
                length_mm,
                centered=(False, False, False),
            )
            .translate((x_start, y_start, z_start))
        )

    def _drawer_child(self, built_cabinet: Any) -> Any:
        return next(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )


__all__ = ["RunnerMovementPreviewGeometry"]
