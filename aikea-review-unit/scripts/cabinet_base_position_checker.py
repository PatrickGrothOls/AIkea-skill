"""Scope: Check one cabinet and its structural base in local and global coordinates."""

from __future__ import annotations

from math import isclose
from typing import Any

from assembly_position_report import AssemblyPositionReport
from door_and_plinth_position_checker import DoorAndPlinthPositionChecker
from physical_part_position_reporter import PhysicalPartPositionReporter
from placed_bounds import PlacedBounds


class CabinetBasePositionChecker:
    """Prove that reviewed assemblies meet through explicit coordinate mappings."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.part_positions = PhysicalPartPositionReporter()
        self.door_and_plinth = DoorAndPlinthPositionChecker()

    def check(
        self,
        built_base: Any,
        built_cabinet: Any,
        base_parts: tuple[Any, ...],
        review_base_parts: tuple[Any, ...],
        cabinet_parts: tuple[Any, ...],
        next_cabinet_spec: Any | None,
    ) -> AssemblyPositionReport:
        base_spec = built_base.spec
        cabinet_spec = built_cabinet.spec
        base_local = PlacedBounds.from_parts(base_parts)
        review_base_local = PlacedBounds.from_parts(review_base_parts)
        carcass_parts = tuple(
            part for part in cabinet_parts if part.name != "door_panel"
        )
        cabinet_local = PlacedBounds.from_parts(carcass_parts)
        deck_local = PlacedBounds.from_parts(
            part for part in base_parts if part.name == "deck_01"
        )
        side_local = PlacedBounds.from_parts(
            part for part in cabinet_parts if part.name in {"left_side", "right_side"}
        )
        lower_front = self.door_and_plinth.check(
            built_base,
            built_cabinet,
            base_parts,
            cabinet_parts,
        )

        base_zero = (float(base_spec.global_left_mm), 0.0, 0.0)
        cabinet_zero = (float(cabinet_spec.global_left_mm), 0.0, 0.0)
        base_global = base_local.shifted(base_zero)
        cabinet_global = cabinet_local.shifted(cabinet_zero)
        deck_global = deck_local.shifted(base_zero)
        first_module_end_global_mm = (
            base_zero[0] + float(base_spec.modules[0].end_x_mm)
        )
        projection_mm = first_module_end_global_mm - float(
            cabinet_spec.global_right_mm
        )
        next_gap_mm = self._next_gap_mm(cabinet_spec, next_cabinet_spec)

        assemblies = {
            base_spec.assembly_id: AssemblyPositionReport.assembly_values(
                base_zero,
                base_local,
                base_global,
                self.part_positions.base_positions(built_base),
            ),
            cabinet_spec.assembly_id: AssemblyPositionReport.assembly_values(
                cabinet_zero,
                cabinet_local,
                cabinet_global,
                self.part_positions.cabinet_positions(built_cabinet),
            ),
        }
        relationships = {
            "base_top_z_mm": base_local.z_max_mm,
            "cabinet_carcass_bottom_z_mm": cabinet_local.z_min_mm,
            "cabinet_side_bottom_z_mm": side_local.z_min_mm,
            "first_base_module_end_x_global_mm": first_module_end_global_mm,
            "first_cabinet_right_x_global_mm": float(
                cabinet_spec.global_right_mm
            ),
            "first_base_module_projection_into_gap_mm": projection_mm,
            "review_base_right_x_global_mm": (
                base_zero[0] + review_base_local.x_max_mm
            ),
            "next_cabinet_gap_mm": next_gap_mm,
            **lower_front.relationships,
        }
        checks = (
            AssemblyPositionReport.check(
                "base and first cabinet share their global X origin",
                self._same(base_zero[0], cabinet_zero[0]),
            ),
            AssemblyPositionReport.check(
                "base bounds match its global span",
                self._same(base_global.x_min_mm, base_spec.global_left_mm)
                and self._same(base_global.x_max_mm, base_spec.global_right_mm),
            ),
            AssemblyPositionReport.check(
                "cabinet carcass bounds match its global span",
                self._same(cabinet_global.x_min_mm, cabinet_spec.global_left_mm)
                and self._same(cabinet_global.x_max_mm, cabinet_spec.global_right_mm),
            ),
            AssemblyPositionReport.check(
                "base deck covers the cabinet footprint",
                deck_global.covers_xy(cabinet_global, self._TOLERANCE_MM),
            ),
            AssemblyPositionReport.check(
                "cabinet sides meet the base top",
                self._same(side_local.z_min_mm, base_local.z_max_mm),
            ),
            AssemblyPositionReport.check(
                "cabinet carcass does not overlap base material",
                cabinet_local.z_min_mm >= base_local.z_max_mm - self._TOLERANCE_MM,
            ),
            AssemblyPositionReport.check(
                "base and cabinet use the same finished depth",
                self._same(base_spec.depth_mm, cabinet_spec.depth_mm),
            ),
            AssemblyPositionReport.check(
                "first base module ends at the centre of the cabinet gap",
                self._same(projection_mm, next_gap_mm / 2.0),
            ),
            AssemblyPositionReport.check(
                "combined review contains only the first base module",
                review_base_local.matches_x_span(
                    base_spec.modules[0].start_x_mm,
                    base_spec.modules[0].end_x_mm,
                    self._TOLERANCE_MM,
                ),
            ),
            *lower_front.checks,
        )
        return AssemblyPositionReport(assemblies, relationships, checks)

    def _next_gap_mm(self, cabinet_spec: Any, next_spec: Any | None) -> float:
        if next_spec is None:
            return 0.0
        return float(next_spec.global_left_mm) - float(cabinet_spec.global_right_mm)

    def _same(self, left: float, right: float) -> bool:
        return isclose(
            float(left),
            float(right),
            rel_tol=0.0,
            abs_tol=self._TOLERANCE_MM,
        )

__all__ = ["CabinetBasePositionChecker"]
