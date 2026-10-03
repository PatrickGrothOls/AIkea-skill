"""Scope: Articulate exact KA 5332 members with their owning drawer or cabinet."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState
from hettich_ka_5332_mounting_plan import HettichKa5332MountingPlan
from hettich_ka_5332_step_assembly import (
    HettichKa5332SideStepParts,
    HettichKa5332StepAssembly,
)
from unit_mockup import MockupPart


class HettichKa5332ReviewGeometry:
    """Keep cabinet members fixed while the middle and drawer members extend."""

    _CABINET_MEMBER_COLOR = (0.31, 0.33, 0.35, 1.0)
    _MIDDLE_MEMBER_COLOR = (0.48, 0.50, 0.52, 1.0)
    _DRAWER_MEMBER_COLOR = (0.68, 0.69, 0.70, 1.0)
    _DRAWER_COLOR = (0.84, 0.75, 0.62, 1.0)

    def __init__(self) -> None:
        self.motion = DrawerReviewMotion()

    def build_hardware(
        self,
        step: HettichKa5332StepAssembly,
        plan: HettichKa5332MountingPlan,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        drawer_travel_mm = self.motion.extension_mm(state, 500.0)
        middle_travel_mm = drawer_travel_mm / 2.0
        return self._side_parts(
            "left",
            step.left,
            plan.left_runner_translation_mm,
            state,
            drawer_travel_mm,
            middle_travel_mm,
        ) + self._side_parts(
            "right",
            step.right,
            plan.right_runner_translation_mm,
            state,
            drawer_travel_mm,
            middle_travel_mm,
        )

    def build_drawer(
        self,
        box: Any,
        plan: HettichKa5332MountingPlan,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        if state is DrawerReviewState.REMOVED:
            return ()
        travel_mm = self.motion.extension_mm(state, box.spec.side_length_mm)
        x_mm, y_mm, z_mm = plan.drawer_origin_mm
        drawer_location = cq.Location(
            cq.Vector(x_mm, y_mm - travel_mm, z_mm)
        )
        return tuple(
            MockupPart(
                f"drawer__{part.spec.part_id}",
                part.solid,
                drawer_location * part.placement.location(),
                self._DRAWER_COLOR,
            )
            for part in box.parts
        )

    def _side_parts(
        self,
        hand: str,
        members: HettichKa5332SideStepParts,
        translation_mm: tuple[float, float, float],
        state: DrawerReviewState,
        drawer_travel_mm: float,
        middle_travel_mm: float,
    ) -> tuple[MockupPart, ...]:
        fixed = self._part(
            hand,
            "cabinet_member",
            members.cabinet_member,
            translation_mm,
            0.0,
            self._CABINET_MEMBER_COLOR,
        )
        middle = self._part(
            hand,
            "middle_member",
            members.middle_member,
            translation_mm,
            middle_travel_mm if state is DrawerReviewState.OPEN else 0.0,
            self._MIDDLE_MEMBER_COLOR,
        )
        if state is DrawerReviewState.REMOVED:
            return fixed, middle
        drawer = self._part(
            hand,
            "drawer_member",
            members.drawer_member,
            translation_mm,
            drawer_travel_mm if state is DrawerReviewState.OPEN else 0.0,
            self._DRAWER_MEMBER_COLOR,
        )
        return fixed, middle, drawer

    def _part(self, hand, role, shape, translation_mm, travel_mm, color):
        x_mm, y_mm, z_mm = translation_mm
        return MockupPart(
            f"ka_5332__{hand}__{role}__source_cad",
            cq.Workplane(obj=shape),
            cq.Location(cq.Vector(x_mm, y_mm - travel_mm, z_mm)),
            color,
        )


__all__ = ["HettichKa5332ReviewGeometry"]
