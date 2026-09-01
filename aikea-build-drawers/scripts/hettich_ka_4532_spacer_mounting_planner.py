"""Scope: Resolve exact KA 4532 and 13952 frames from cabinet-local faces."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from assembly_part_locator import AssemblyPartLocator
from drawer_hardware_mounting_plan import HardwarePlacement
from hettich_ka_4532_spacer_mounting_plan import (
    HettichKa4532SpacerMountingPlan,
    Vector3D,
)
from hettich_ka_4532_spacer_profile import (
    HETTICH_KA_4532_500_WITH_13952,
    HettichKa4532SpacerProfile,
)
from part_outside_face_plane import PartOutsideFacePlaneResolver

if TYPE_CHECKING:
    from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSet

Axes3D = tuple[Vector3D, Vector3D, Vector3D]


class HettichKa4532SpacerMountingPlanner:
    """Resolve rigid placements without changing either purchased STEP."""

    _IDENTITY_AXES: Axes3D = (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    _RIGHT_SPACER_AXES: Axes3D = (
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, -1.0),
    )

    def __init__(self) -> None:
        self._part_locator = AssemblyPartLocator()
        self._outside_face = PartOutsideFacePlaneResolver()

    def plan(
        self,
        cabinet: Any,
        step_set: HettichKa4532SpacerStepSet,
        *,
        cabinet_front_mm: float,
        drawer_front_mm: float,
        drawer_bottom_mm: float,
        hardware: HettichKa4532SpacerProfile = HETTICH_KA_4532_500_WITH_13952,
    ) -> HettichKa4532SpacerMountingPlan:
        left_inside_mm = self._inside_face_x(cabinet, "left_side")
        right_inside_mm = self._inside_face_x(cabinet, "right_side")
        hardware_width_mm = hardware.hardware_width_per_side_mm
        drawer_origin_mm = (
            left_inside_mm + hardware_width_mm,
            drawer_front_mm,
            drawer_bottom_mm,
        )
        drawer_width_mm = right_inside_mm - left_inside_mm - 2.0 * hardware_width_mm
        left_contact_mm = left_inside_mm + hardware.spacer_width_per_side_mm
        right_contact_mm = right_inside_mm - hardware.spacer_width_per_side_mm
        left_runner_x_mm = (
            left_contact_mm - step_set.runner_left.fixed_member.BoundingBox().xmin
        )
        right_runner_x_mm = (
            right_contact_mm - step_set.runner_right.fixed_member.BoundingBox().xmax
        )
        runner_bounds = step_set.runner_source.bounds_mm
        runner_z_mm = (
            drawer_bottom_mm
            + hardware.runner_center_from_drawer_bottom_mm
            - (runner_bounds.zmin + runner_bounds.zmax) / 2.0
        )
        return HettichKa4532SpacerMountingPlan(
            cabinet_front_mm=cabinet_front_mm,
            drawer_front_mm=drawer_front_mm,
            drawer_origin_mm=drawer_origin_mm,
            drawer_outside_width_mm=drawer_width_mm,
            spacer_left_in_cabinet=self._placement(
                (
                    left_inside_mm,
                    cabinet_front_mm + hardware.spacer_front_from_cabinet_front_mm,
                    drawer_bottom_mm + hardware.spacer_bottom_from_drawer_bottom_mm,
                ),
                self._IDENTITY_AXES,
            ),
            spacer_right_in_cabinet=self._placement(
                (
                    right_inside_mm,
                    cabinet_front_mm + hardware.spacer_front_from_cabinet_front_mm,
                    drawer_bottom_mm
                    + hardware.spacer_bottom_from_drawer_bottom_mm
                    + hardware.spacer_height_mm,
                ),
                self._RIGHT_SPACER_AXES,
            ),
            fixed_runner_left_in_cabinet=self._runner_placement(
                step_set.runner_left.fixed_member,
                left_runner_x_mm,
                cabinet_front_mm + hardware.runner_front_from_drawer_front_mm,
                runner_z_mm,
            ),
            fixed_runner_right_in_cabinet=self._runner_placement(
                step_set.runner_right.fixed_member,
                right_runner_x_mm,
                cabinet_front_mm + hardware.runner_front_from_drawer_front_mm,
                runner_z_mm,
            ),
            moving_runner_left_in_drawer=self._runner_placement(
                step_set.runner_left.moving_member,
                left_runner_x_mm - drawer_origin_mm[0],
                hardware.runner_front_from_drawer_front_mm,
                runner_z_mm - drawer_bottom_mm,
            ),
            moving_runner_right_in_drawer=self._runner_placement(
                step_set.runner_right.moving_member,
                right_runner_x_mm - drawer_origin_mm[0],
                hardware.runner_front_from_drawer_front_mm,
                runner_z_mm - drawer_bottom_mm,
            ),
        )

    def _runner_placement(
        self,
        member: Any,
        x_translation_mm: float,
        front_mm: float,
        z_translation_mm: float,
    ) -> HardwarePlacement:
        native_front_mm = member.BoundingBox().ymin
        return self._placement(
            (x_translation_mm, front_mm - native_front_mm, z_translation_mm),
            self._IDENTITY_AXES,
        )

    def _inside_face_x(self, cabinet: Any, part_id: str) -> float:
        part = cabinet.part(part_id)
        location = self._part_locator.locate(part, cabinet, cabinet.base_height_mm)
        outside = self._outside_face.resolve(part, location)
        thickness_mm = float(part.local_size_mm[2])
        return float((outside.center - outside.normal.multiply(thickness_mm)).x)

    def _placement(self, origin_mm: Vector3D, axes: Axes3D) -> HardwarePlacement:
        return HardwarePlacement(origin_mm, axes[0], axes[1], axes[2])

__all__ = ["HettichKa4532SpacerMountingPlanner"]
