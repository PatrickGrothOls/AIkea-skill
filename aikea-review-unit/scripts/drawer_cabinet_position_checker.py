"""Scope: Prove one built drawer child fits its cabinet and global frame."""

from __future__ import annotations

from typing import Any

from assembly_position_report import AssemblyPositionReport
from drawer_cabinet_clearance import DrawerCabinetClearance
from movento_runner_catalog import MOVENTO_RUNNER_CATALOG
from placed_bounds import PlacedBounds


class DrawerCabinetPositionChecker:
    """Check the closed drawer before any open presentation transform."""

    def __init__(self) -> None:
        self.clearance = DrawerCabinetClearance()

    def check(
        self,
        built_cabinet: Any,
        cabinet_parts: tuple[Any, ...],
        drawer_parts: tuple[Any, ...],
    ) -> AssemblyPositionReport:
        cabinet = built_cabinet.spec
        child = self._drawer_child(built_cabinet)
        box = child.assembly.spec.box
        origin = child.spec.local_to_parent.origin_in_parent
        cabinet_bounds = PlacedBounds.from_parts(cabinet_parts)
        drawer_bounds = PlacedBounds.from_parts(drawer_parts)
        drawer_local_bounds = PlacedBounds(
            0.0,
            box.outside_width_mm,
            0.0,
            box.outside_depth_mm,
            0.0,
            box.sizing.box_height_mm,
        )
        global_offset = (float(cabinet.global_left_mm), 0.0, 0.0)
        drawer_global = drawer_bounds.shifted(global_offset)
        inner_bounds = self.clearance.inner_bounds(cabinet)
        collisions = self.clearance.collisions(cabinet_parts, drawer_parts)
        runner = next(
            profile
            for profile in MOVENTO_RUNNER_CATALOG.profiles
            if profile.product_code == child.assembly.spec.runner_product_code
        )
        required_depth_mm = runner.required_inside_depth_mm(
            box.sizing.front_back_thickness_mm
        )
        checks = (
            AssemblyPositionReport.check(
                "closed drawer stays inside the cabinet opening",
                self.clearance.contains(inner_bounds, drawer_bounds),
            ),
            AssemblyPositionReport.check(
                "selected runner depth fits the cabinet",
                required_depth_mm <= float(cabinet.inside_depth_mm),
            ),
            AssemblyPositionReport.check(
                "drawer material does not overlap cabinet material",
                not collisions,
            ),
        )
        local_zero = (origin.x_mm, origin.y_mm, origin.z_mm)
        global_zero = (origin.x_mm + global_offset[0], origin.y_mm, origin.z_mm)
        basis = child.spec.local_to_parent.axis_basis
        assemblies = {
            cabinet.assembly_id: AssemblyPositionReport.assembly_values(
                global_offset,
                cabinet_bounds,
                cabinet_bounds.shifted(global_offset),
                {},
            ),
            child.spec.assembly_id: AssemblyPositionReport.assembly_values(
                global_zero,
                drawer_local_bounds,
                drawer_global,
                self.clearance.part_positions(drawer_parts, global_offset),
            ),
        }
        relationships = {
            "parent_assembly_id": cabinet.assembly_id,
            "drawer_local_zero_in_cabinet_mm": list(local_zero),
            "drawer_local_axes_in_cabinet": {
                "x": self._axis_values(basis.local_x_in_parent),
                "y": self._axis_values(basis.local_y_in_parent),
                "z": self._axis_values(basis.local_z_in_parent),
            },
            "runner_product_code": runner.product_code,
            "runner_required_depth_mm": required_depth_mm,
            "hardware_geometry": child.assembly.spec.hardware_geometry_state,
            "runner_frame_owner": cabinet.assembly_id,
            "review_motion_owner": child.spec.assembly_id,
            "closed_clearances_mm": self.clearance.clearances(
                inner_bounds,
                drawer_bounds,
            ),
            "material_collisions": [list(pair) for pair in collisions],
        }
        return AssemblyPositionReport(assemblies, relationships, checks)

    def _drawer_child(self, built_cabinet: Any) -> Any:
        return next(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )

    def _axis_values(self, direction: Any) -> list[float]:
        return [direction.x, direction.y, direction.z]

__all__ = ["DrawerCabinetPositionChecker"]
