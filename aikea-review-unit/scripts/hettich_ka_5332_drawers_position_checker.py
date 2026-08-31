"""Scope: Check every closed drawer child in one cabinet and global frame."""

from __future__ import annotations

from itertools import combinations
from typing import Any

from assembly_position_report import AssemblyPositionReport
from drawer_cabinet_clearance import DrawerCabinetClearance
from placed_bounds import PlacedBounds


class HettichKa5332DrawersPositionChecker:
    """Prove independent drawer children fit the cabinet and one another."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.clearance = DrawerCabinetClearance()

    def check(
        self,
        built_cabinet: Any,
        cabinet_parts: tuple[Any, ...],
        drawer_parts: tuple[Any, ...],
    ) -> AssemblyPositionReport:
        cabinet = built_cabinet.spec
        inner_bounds = self.clearance.inner_bounds(cabinet)
        cabinet_bounds = PlacedBounds.from_parts(cabinet_parts)
        global_offset = (float(cabinet.global_left_mm), 0.0, 0.0)
        assemblies = {
            cabinet.assembly_id: AssemblyPositionReport.assembly_values(
                global_offset,
                cabinet_bounds,
                cabinet_bounds.shifted(global_offset),
                {},
            )
        }
        checks: list[dict[str, Any]] = []
        relationships: dict[str, Any] = {"drawers": {}}
        grouped = {
            child.spec.assembly_id: tuple(
                part
                for part in drawer_parts
                if part.name.startswith(child.spec.assembly_id + "__")
            )
            for child in self._drawer_children(built_cabinet)
        }
        for child in self._drawer_children(built_cabinet):
            drawer_id = child.spec.assembly_id
            parts = grouped[drawer_id]
            bounds = PlacedBounds.from_parts(parts)
            collisions = self.clearance.collisions(cabinet_parts, parts)
            checks.extend(
                (
                    AssemblyPositionReport.check(
                        f"{drawer_id} stays inside the cabinet opening",
                        self.clearance.contains(inner_bounds, bounds),
                    ),
                    AssemblyPositionReport.check(
                        f"{drawer_id} material does not overlap cabinet material",
                        not collisions,
                    ),
                )
            )
            origin = child.spec.local_to_parent.origin_in_parent
            local_zero = (origin.x_mm, origin.y_mm, origin.z_mm)
            global_zero = (origin.x_mm + global_offset[0], origin.y_mm, origin.z_mm)
            assemblies[drawer_id] = AssemblyPositionReport.assembly_values(
                global_zero,
                self._local_bounds(child),
                bounds.shifted(global_offset),
                self.clearance.part_positions(parts, global_offset),
            )
            relationships["drawers"][drawer_id] = {
                "local_zero_in_cabinet_mm": list(local_zero),
                "closed_clearances_mm": self.clearance.clearances(inner_bounds, bounds),
                "material_collisions": [list(pair) for pair in collisions],
            }
        pair_collisions = self._drawer_collisions(grouped)
        checks.append(
            AssemblyPositionReport.check(
                "closed drawers do not overlap one another",
                not pair_collisions,
            )
        )
        relationships["drawer_collisions"] = [list(pair) for pair in pair_collisions]
        return AssemblyPositionReport(assemblies, relationships, tuple(checks))

    def _drawer_children(self, built_cabinet: Any) -> tuple[Any, ...]:
        return tuple(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )

    def _local_bounds(self, child: Any) -> PlacedBounds:
        box = child.assembly.spec.box
        return PlacedBounds(
            0.0,
            box.outside_width_mm,
            0.0,
            box.outside_depth_mm,
            0.0,
            box.sizing.box_height_mm,
        )

    def _drawer_collisions(self, grouped) -> tuple[tuple[str, str], ...]:
        return tuple(
            (left_id, right_id)
            for (left_id, left), (right_id, right) in combinations(grouped.items(), 2)
            if any(
                left_part.placed_shape().intersect(right_part.placed_shape()).Volume()
                > self._TOLERANCE_MM
                for left_part in left
                for right_part in right
            )
        )


__all__ = ["HettichKa5332DrawersPositionChecker"]
