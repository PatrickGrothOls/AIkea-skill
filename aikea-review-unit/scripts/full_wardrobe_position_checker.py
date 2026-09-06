"""Scope: Check the complete cabinet run and base in project coordinates."""

from __future__ import annotations

from math import isclose
from typing import Any

from assembly_position_report import AssemblyPositionReport
from cabinet_on_base_position_checker import CabinetOnBasePositionChecker
from physical_part_position_reporter import PhysicalPartPositionReporter
from placed_bounds import PlacedBounds


class FullWardrobePositionChecker:
    """Prove every cabinet occupies its saved span and bears on the full base."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.part_positions = PhysicalPartPositionReporter()
        self.cabinet_checker = CabinetOnBasePositionChecker()

    def check(
        self,
        built_base: Any,
        base_parts: tuple[Any, ...],
        built_cabinets: tuple[Any, ...],
        cabinet_parts: tuple[tuple[Any, ...], ...],
    ) -> AssemblyPositionReport:
        base = built_base.spec
        base_local = PlacedBounds.from_parts(base_parts)
        base_zero = (float(base.global_left_mm), 0.0, 0.0)
        base_global = base_local.shifted(base_zero)
        deck_local = PlacedBounds.from_parts(
            part for part in base_parts if part.name.startswith("deck_")
        )
        deck_global = deck_local.shifted(base_zero)
        front_rail = PlacedBounds.from_parts(
            part for part in base_parts if part.name.startswith("front_rail_")
        )
        assemblies = {
            base.assembly_id: AssemblyPositionReport.assembly_values(
                base_zero,
                base_local,
                base_global,
                self.part_positions.base_positions(built_base),
            )
        }
        relationships: dict[str, Any] = {
            "cabinet_count": len(built_cabinets),
            "base_top_z_mm": base_local.z_max_mm,
            "plinth_front": base.plinth_front,
            "plinth_recess_mm": float(base.plinth_recess_mm),
            "plinth_front_y_mm": front_rail.y_min_mm,
            "cabinet_gaps_mm": self._cabinet_gaps(built_cabinets),
            "door_bottoms_z_mm": {},
        }
        checks = [
            AssemblyPositionReport.check(
                "base spans the complete cabinet run",
                self._same(base.global_left_mm, built_cabinets[0].spec.global_left_mm)
                and self._same(base.global_right_mm, built_cabinets[-1].spec.global_right_mm),
            ),
            AssemblyPositionReport.check(
                "plinth front reaches its selected depth",
                self._same(front_rail.y_min_mm, base.plinth_recess_mm),
            ),
        ]
        for built, parts in zip(built_cabinets, cabinet_parts):
            result = self.cabinet_checker.check(
                built,
                parts,
                base,
                base_local,
                deck_global,
            )
            assemblies[result.assembly_id] = result.assembly_values
            relationships["door_bottoms_z_mm"][result.assembly_id] = (
                result.door_bottom_z_mm
            )
            checks.extend(result.checks)
        checks.extend(self._gap_checks(built_cabinets))
        return AssemblyPositionReport(assemblies, relationships, tuple(checks))

    def _cabinet_gaps(self, cabinets: tuple[Any, ...]) -> list[float]:
        return [
            float(right.spec.global_left_mm) - float(left.spec.global_right_mm)
            for left, right in zip(cabinets, cabinets[1:])
        ]

    def _gap_checks(self, cabinets: tuple[Any, ...]) -> list[dict[str, Any]]:
        return [
            AssemblyPositionReport.check(
                f"{left.spec.assembly_id} and {right.spec.assembly_id} do not overlap",
                float(left.spec.global_right_mm) <= float(right.spec.global_left_mm),
            )
            for left, right in zip(cabinets, cabinets[1:])
        ]

    def _same(self, left: float, right: float) -> bool:
        return isclose(
            float(left),
            float(right),
            rel_tol=0.0,
            abs_tol=self._TOLERANCE_MM,
        )


__all__ = ["FullWardrobePositionChecker"]
