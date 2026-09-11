"""Scope: Resolve MOVENTO runner and locking-device frames from one drawer plan."""

from __future__ import annotations

from typing import Any

from drawer_hardware_mounting_plan import (
    DrawerHardwareMountingPlan,
    HardwarePlacement,
)
from movento_mounting_profile import MoventoMountingProfile
from drawer_host import DrawerHost

Vector3D = tuple[float, float, float]


class MoventoHardwareMountingPlanner:
    """Align handed source CAD through the shared cabinet-side datum."""

    def plan(
        self,
        cabinet: Any,
        drawer_box: Any,
        drawer_origin_in_cabinet_mm: Vector3D,
        profile: MoventoMountingProfile,
    ) -> DrawerHardwareMountingPlan:
        host = DrawerHost.resolve(cabinet)
        left_wall_mm, right_wall_mm = host.inside_x("left"), host.inside_x("right")
        side_clearance_mm = (
            drawer_box.opening.clear_width_mm - drawer_box.outside_width_mm
        ) / 2.0
        depth_in_drawer_mm = profile.drawer_front_to_manufacturer_origin_mm
        height_in_drawer_mm = profile.drawer_bottom_to_manufacturer_origin_mm
        shared_axes = (
            profile.native_x_in_owner,
            profile.native_y_in_owner,
            profile.native_z_in_owner,
        )
        parent_depth_mm = drawer_origin_in_cabinet_mm[1] + depth_in_drawer_mm
        parent_height_mm = drawer_origin_in_cabinet_mm[2] + height_in_drawer_mm
        return DrawerHardwareMountingPlan(
            runner_left_in_cabinet=self._placement(
                (left_wall_mm, parent_depth_mm, parent_height_mm), shared_axes
            ),
            runner_right_in_cabinet=self._placement(
                (right_wall_mm, parent_depth_mm, parent_height_mm), shared_axes
            ),
            locking_device_left_in_drawer=self._placement(
                (-side_clearance_mm, depth_in_drawer_mm, height_in_drawer_mm),
                shared_axes,
            ),
            locking_device_right_in_drawer=self._placement(
                (
                    drawer_box.outside_width_mm + side_clearance_mm,
                    depth_in_drawer_mm,
                    height_in_drawer_mm,
                ),
                shared_axes,
            ),
        )

    def _placement(
        self,
        origin_mm: Vector3D,
        axes: tuple[Vector3D, Vector3D, Vector3D],
    ) -> HardwarePlacement:
        return HardwarePlacement(origin_mm, axes[0], axes[1], axes[2])


__all__ = ["MoventoHardwareMountingPlanner", "Vector3D"]
