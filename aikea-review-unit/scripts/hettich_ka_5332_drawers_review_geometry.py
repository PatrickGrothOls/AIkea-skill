"""Scope: Pose independent saved drawers and exact KA 5332 runner members."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import cadquery as cq

from hettich_ka_5332_saved_drawers_loader import HettichKa5332SavedDrawer
from hettich_ka_5332_step_assembly import HettichKa5332SideStepParts
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart, UnitMockupInputError


class HettichKa5332DrawersReviewGeometry:
    """Move each drawer by its own review distance while its cabinet rail stays fixed."""

    _CABINET_MEMBER_COLOR = (0.31, 0.33, 0.35, 1.0)
    _MIDDLE_MEMBER_COLOR = (0.48, 0.50, 0.52, 1.0)
    _DRAWER_MEMBER_COLOR = (0.68, 0.69, 0.70, 1.0)
    _DRAWER_COLOR = (0.84, 0.75, 0.62, 1.0)

    def __init__(self) -> None:
        self.frame_location = LocalToParentLocation()

    def build_drawers(
        self,
        drawers: tuple[HettichKa5332SavedDrawer, ...],
        extensions_mm: Mapping[str, float],
    ) -> tuple[MockupPart, ...]:
        return tuple(
            part
            for drawer in drawers
            for part in self._drawer_parts(
                drawer,
                float(extensions_mm.get(drawer.drawer_id, 0.0)),
            )
        )

    def build_hardware(
        self,
        drawers: tuple[HettichKa5332SavedDrawer, ...],
        steps_by_item_number: Mapping[str, Any],
        extensions_mm: Mapping[str, float],
    ) -> tuple[MockupPart, ...]:
        return tuple(
            part
            for drawer in drawers
            for part in self._hardware_parts(
                drawer,
                steps_by_item_number[drawer.runner_item_number],
                float(extensions_mm.get(drawer.drawer_id, 0.0)),
            )
        )

    def _drawer_parts(
        self,
        drawer: HettichKa5332SavedDrawer,
        extension_mm: float,
    ) -> tuple[MockupPart, ...]:
        box = drawer.child.assembly.spec.box
        self._require_extension(drawer.drawer_id, extension_mm, box.side_length_mm)
        child_frame = self.frame_location.build(
            drawer.child.spec.local_to_parent
        )
        motion = cq.Location(cq.Vector(0.0, -extension_mm, 0.0))
        return tuple(
            MockupPart(
                f"{drawer.drawer_id}__{part.spec.part_id}",
                part.solid,
                child_frame
                * motion
                * self.frame_location.build(part.spec.local_to_parent),
                self._DRAWER_COLOR,
            )
            for part in drawer.child.assembly.parts
        )

    def _hardware_parts(self, drawer, step, extension_mm):
        middle_extension_mm = extension_mm / 2.0
        plan = drawer.mounting
        return self._side_parts(
            drawer.drawer_id,
            "left",
            step.left,
            plan.left_runner_translation_mm,
            extension_mm,
            middle_extension_mm,
        ) + self._side_parts(
            drawer.drawer_id,
            "right",
            step.right,
            plan.right_runner_translation_mm,
            extension_mm,
            middle_extension_mm,
        )

    def _side_parts(
        self,
        drawer_id: str,
        hand: str,
        members: HettichKa5332SideStepParts,
        origin_mm,
        drawer_extension_mm: float,
        middle_extension_mm: float,
    ) -> tuple[MockupPart, ...]:
        return tuple(
            self._hardware_part(drawer_id, hand, role, shape, origin_mm, travel, color)
            for role, shape, travel, color in (
                ("cabinet_member", members.cabinet_member, 0.0, self._CABINET_MEMBER_COLOR),
                ("middle_member", members.middle_member, middle_extension_mm, self._MIDDLE_MEMBER_COLOR),
                ("drawer_member", members.drawer_member, drawer_extension_mm, self._DRAWER_MEMBER_COLOR),
            )
        )

    def _hardware_part(self, drawer_id, hand, role, shape, origin_mm, travel_mm, color):
        x_mm, y_mm, z_mm = origin_mm
        return MockupPart(
            f"{drawer_id}__ka_5332__{hand}__{role}__source_cad",
            cq.Workplane(obj=shape),
            cq.Location(cq.Vector(x_mm, y_mm - travel_mm, z_mm)),
            color,
        )

    def _require_extension(self, drawer_id: str, extension_mm: float, depth_mm: float) -> None:
        if extension_mm < 0.0 or extension_mm > depth_mm:
            raise UnitMockupInputError(
                [f"{drawer_id} review extension must be between 0 and {depth_mm:g} mm"]
            )


__all__ = ["HettichKa5332DrawersReviewGeometry"]
