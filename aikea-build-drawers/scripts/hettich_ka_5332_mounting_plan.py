"""Scope: Place the exact KA 5332 pair between cabinet and drawer side faces."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hettich_ka_5332_runner_profile import HettichKa5332RunnerProfile
from hettich_ka_5332_step_assembly import HettichKa5332StepAssembly

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class HettichKa5332MountingPlan:
    """Carry drawer and vendor-STEP translations in the cabinet frame."""

    drawer_origin_mm: Vector3D
    drawer_outside_width_mm: float
    left_runner_translation_mm: Vector3D
    right_runner_translation_mm: Vector3D
    system_32_row_height_mm: float
    resolved_drawer_bottom_height_mm: float
    recommended_width_met: bool
    minimum_depth_met: bool


class HettichKa5332MountingPlanner:
    """Align rail contact faces from cabinet dimensions and vendor bounds."""

    def plan(
        self,
        cabinet_spec: Any,
        step: HettichKa5332StepAssembly,
        runner: HettichKa5332RunnerProfile,
        *,
        drawer_front_mm: float,
        drawer_bottom_mm: float,
        system_32_row_height_mm: float,
    ) -> HettichKa5332MountingPlan:
        left_inside_mm = float(cabinet_spec.part("left_side").local_size_mm[2])
        right_inside_mm = float(cabinet_spec.width_mm) - float(
            cabinet_spec.part("right_side").local_size_mm[2]
        )
        clear_width_mm = right_inside_mm - left_inside_mm
        drawer_width_mm = clear_width_mm - (
            2.0 * runner.installed_width_per_side_mm
        )
        common_y_mm = (
            drawer_front_mm + runner.manufacturer_origin_from_drawer_front_mm
        )
        common_z_mm = (
            drawer_bottom_mm + runner.runner_center_from_drawer_bottom_mm
        )
        left_x_mm = (
            left_inside_mm
            - step.left.cabinet_member.BoundingBox().xmin
        )
        right_x_mm = (
            right_inside_mm
            - step.right.cabinet_member.BoundingBox().xmax
        )
        return HettichKa5332MountingPlan(
            drawer_origin_mm=(
                left_inside_mm + runner.installed_width_per_side_mm,
                drawer_front_mm,
                drawer_bottom_mm,
            ),
            drawer_outside_width_mm=drawer_width_mm,
            left_runner_translation_mm=(left_x_mm, common_y_mm, common_z_mm),
            right_runner_translation_mm=(right_x_mm, common_y_mm, common_z_mm),
            system_32_row_height_mm=system_32_row_height_mm,
            resolved_drawer_bottom_height_mm=(
                system_32_row_height_mm
                - runner.runner_center_from_drawer_bottom_mm
            ),
            recommended_width_met=(
                drawer_width_mm <= runner.recommended_maximum_drawer_width_mm
            ),
            minimum_depth_met=(
                float(cabinet_spec.inside_depth_mm)
                >= runner.minimum_cabinet_depth_mm
            ),
        )


__all__ = ["HettichKa5332MountingPlan", "HettichKa5332MountingPlanner"]
