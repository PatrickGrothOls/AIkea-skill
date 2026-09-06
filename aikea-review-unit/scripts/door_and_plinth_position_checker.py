"""Scope: Check the selected door bottom and plinth front in placed geometry."""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose
from typing import Any

from assembly_position_report import AssemblyPositionReport
from placed_bounds import PlacedBounds


@dataclass(frozen=True)
class DoorAndPlinthPositionResult:
    """Carry lower-front relationships into the complete position report."""

    relationships: dict[str, Any]
    checks: tuple[dict[str, Any], ...]


class DoorAndPlinthPositionChecker:
    """Prove that both independent design choices reached physical geometry."""

    _TOLERANCE_MM = 1e-6

    def check(
        self,
        built_base: Any,
        built_cabinet: Any,
        base_parts: tuple[Any, ...],
        cabinet_parts: tuple[Any, ...],
    ) -> DoorAndPlinthPositionResult:
        base = built_base.spec
        cabinet = built_cabinet.spec
        front_rail = PlacedBounds.from_parts(
            part for part in base_parts if part.name == "front_rail_01"
        )
        deck = PlacedBounds.from_parts(
            part for part in base_parts if part.name == "deck_01"
        )
        door = PlacedBounds.from_parts(
            part for part in cabinet_parts if part.name == "door_panel"
        )
        selected_door_bottom_mm = self._selected_door_bottom(cabinet, deck)
        relationships = {
            "door_bottom": cabinet.door_bottom,
            "door_bottom_z_mm": door.z_min_mm,
            "plinth_front": base.plinth_front,
            "plinth_recess_mm": float(base.plinth_recess_mm),
            "plinth_front_y_mm": front_rail.y_min_mm,
            "base_deck_bottom_z_mm": deck.z_min_mm,
        }
        checks = (
            AssemblyPositionReport.check(
                "door reaches its selected lower line",
                self._same(door.z_min_mm, selected_door_bottom_mm),
            ),
            AssemblyPositionReport.check(
                "plinth front reaches its selected depth",
                self._same(front_rail.y_min_mm, base.plinth_recess_mm),
            ),
        )
        return DoorAndPlinthPositionResult(relationships, checks)

    def _selected_door_bottom(self, cabinet: Any, deck: PlacedBounds) -> float:
        return 0.0 if cabinet.door_bottom == "floor" else deck.z_min_mm

    def _same(self, left: float, right: float) -> bool:
        return isclose(
            float(left),
            float(right),
            rel_tol=0.0,
            abs_tol=self._TOLERANCE_MM,
        )


__all__ = ["DoorAndPlinthPositionChecker", "DoorAndPlinthPositionResult"]
