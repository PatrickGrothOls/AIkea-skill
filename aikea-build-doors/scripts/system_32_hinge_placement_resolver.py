"""Scope: Fit one door's mounting plates onto its cabinet's shared System 32 grid."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from door_host import DoorHost
from door_hinge_spread_policy import DoorHingeSpreadPolicy
from door_hinge_side import DoorHingeSide
from panel_hardware_reservation import PanelHardwareReservation
from riex_nc70_hardware_clearance import RiexNc70HardwareClearance
from riex_nc70_hinge_profile import (
    RIEX_NC70_FULL_OVERLAY,
    RiexNc70HingeProfile,
)
from system_32_side_panel_grid import System32SidePanelGrid


class System32HingePlacementError(ValueError):
    """Report a door whose cabinet grid cannot accept the required plates."""


@dataclass(frozen=True, slots=True)
class System32PlatePosition:
    """Name one adjacent grid pair and its matching door center."""

    cabinet_fixing_rows_mm: tuple[float, float]
    cabinet_center_mm: float
    door_center_mm: float


class System32HingePlacementResolver:
    """Choose grid pairs near the ideal spread while avoiding cabinet features."""

    def __init__(self, grid: System32SidePanelGrid | None = None) -> None:
        self.grid = grid or System32SidePanelGrid()
        self.spread = DoorHingeSpreadPolicy()
        self.hardware_clearance = RiexNc70HardwareClearance()

    def resolve(
        self,
        assembly: Any,
        hinge_count: int,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
        profile: RiexNc70HingeProfile = RIEX_NC70_FULL_OVERLAY,
        blocked_reservations: tuple[PanelHardwareReservation, ...] = (),
    ) -> tuple[System32PlatePosition, ...]:
        host = DoorHost.resolve(assembly, hinge_side)
        door_height_mm = host.dimensions[hinge_side.door_height_dimension]
        side_height_mm = host.support.local_size_mm[1]
        cabinet_offset_mm = host.door_bottom_mm-host.support_bottom_mm
        obstacles = blocked_reservations + host.fixed_reservations
        candidates = tuple(
            self._position(pair, cabinet_offset_mm)
            for pair in self.grid.adjacent_row_pairs_mm(side_height_mm)
        )
        candidates = tuple(
            position
            for position in candidates
            if self.spread.contains(position.door_center_mm, door_height_mm)
            and self.hardware_clearance.clears(
                position,
                hinge_side,
                profile,
                obstacles, host,
            )
        )
        selected: list[System32PlatePosition] = []
        selected_reservations: list[PanelHardwareReservation] = []
        for target_mm in self.spread.ideal_centers_mm(door_height_mm, hinge_count):
            available = tuple(
                item
                for item in candidates
                if item not in selected
                and self.hardware_clearance.clears(
                    item,
                    hinge_side,
                    profile,
                    tuple(selected_reservations), host,
                )
            )
            if not available:
                raise System32HingePlacementError(
                    "cabinet System 32 grid has no clear adjacent pair for every hinge"
                )
            position = min(
                available,
                key=lambda item: (
                    abs(item.door_center_mm - target_mm),
                    item.door_center_mm,
                ),
            )
            selected.append(position)
            selected_reservations.append(
                self.hardware_clearance.reservation(
                    "selected_hinge_plate",
                    position,
                    hinge_side,
                    profile, host,
                )
            )
        return tuple(sorted(selected, key=lambda item: item.door_center_mm))

    def _position(
        self,
        rows_mm: tuple[float, float],
        cabinet_offset_mm: float,
    ) -> System32PlatePosition:
        cabinet_center_mm = sum(rows_mm) / 2.0
        return System32PlatePosition(
            cabinet_fixing_rows_mm=rows_mm,
            cabinet_center_mm=cabinet_center_mm,
            door_center_mm=cabinet_center_mm - cabinet_offset_mm,
        )

__all__ = [
    "System32HingePlacementError",
    "System32HingePlacementResolver",
    "System32PlatePosition",
]
