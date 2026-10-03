"""Scope: Check one closed cabinet against the complete structural base."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Any

from assembly_position_report import AssemblyPositionReport
from physical_part_position_reporter import PhysicalPartPositionReporter
from placed_bounds import PlacedBounds


@dataclass(frozen=True)
class CabinetOnBasePositionResult:
    assembly_id: str
    assembly_values: dict[str, Any]
    door_bottom_z_mm: float
    checks: tuple[dict[str, Any], ...]


class CabinetOnBasePositionChecker:
    """Prove one cabinet occupies its span and bears on the shared deck."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.part_positions = PhysicalPartPositionReporter()

    def check(
        self,
        built: Any,
        parts: tuple[Any, ...],
        base: Any,
        base_local: PlacedBounds,
        deck_global: PlacedBounds,
    ) -> CabinetOnBasePositionResult:
        spec = built.spec
        carcass = PlacedBounds.from_parts(
            part for part in parts if part.name != "door_panel"
        )
        sides = PlacedBounds.from_parts(
            part for part in parts if part.name in {"left_side", "right_side"}
        )
        door = PlacedBounds.from_parts(
            part for part in parts if part.name == "door_panel"
        )
        global_zero = (float(spec.global_left_mm), 0.0, 0.0)
        global_bounds = carcass.shifted(global_zero)
        assembly_values = AssemblyPositionReport.assembly_values(
            global_zero,
            carcass,
            global_bounds,
            self.part_positions.cabinet_positions(built),
        )
        checks = (
            AssemblyPositionReport.check(
                f"{spec.assembly_id} matches its saved width span",
                self._same(global_bounds.x_min_mm, spec.global_left_mm)
                and self._same(global_bounds.x_max_mm, spec.global_right_mm),
            ),
            AssemblyPositionReport.check(
                f"{spec.assembly_id} bears on the base deck",
                self._same(sides.z_min_mm, base_local.z_max_mm)
                and deck_global.covers_xy(global_bounds, self._TOLERANCE_MM),
            ),
            AssemblyPositionReport.check(
                f"{spec.assembly_id} carcass does not overlap base material",
                carcass.z_min_mm >= base_local.z_max_mm - self._TOLERANCE_MM,
            ),
            AssemblyPositionReport.check(
                f"{spec.assembly_id} uses the shared finished depth",
                self._same(spec.depth_mm, base.depth_mm),
            ),
            AssemblyPositionReport.check(
                f"{spec.assembly_id} door reaches its selected lower line",
                self._same(door.z_min_mm, spec.door_bottom_mm),
            ),
        )
        return CabinetOnBasePositionResult(
            spec.assembly_id,
            assembly_values,
            door.z_min_mm,
            checks,
        )

    def _same(self, left: float, right: float) -> bool:
        return isclose(
            float(left),
            float(right),
            rel_tol=0.0,
            abs_tol=self._TOLERANCE_MM,
        )


__all__ = ["CabinetOnBasePositionChecker", "CabinetOnBasePositionResult"]
