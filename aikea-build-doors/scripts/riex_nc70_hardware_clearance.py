"""Scope: Check one proposed Riex plate against reserved side-panel hardware."""

from __future__ import annotations

from typing import Any

from door_hinge_side import DoorHingeSide
from panel_hardware_reservation import (
    PanelHardwareConflictError,
    PanelHardwareReservation,
    PanelHardwareReservationPlan,
)
from riex_nc70_hardware_reservations import RiexNc70HardwareReservations
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class RiexNc70HardwareClearance:
    """Translate candidate positions into reservations before comparison."""

    def __init__(self) -> None:
        self.reservations = RiexNc70HardwareReservations()
        self.compatibility = PanelHardwareReservationPlan()

    def clears(
        self,
        position: Any,
        hinge_side: DoorHingeSide,
        profile: RiexNc70HingeProfile,
        existing: tuple[PanelHardwareReservation, ...],
    ) -> bool:
        candidate = self.reservation(
            "candidate_hinge_plate",
            position,
            hinge_side,
            profile,
        )
        try:
            self.compatibility.require_compatible(candidate, existing)
        except PanelHardwareConflictError:
            return False
        return True

    def reservation(
        self,
        owner_id: str,
        position: Any,
        hinge_side: DoorHingeSide,
        profile: RiexNc70HingeProfile,
    ) -> PanelHardwareReservation:
        return self.reservations.for_position(
            owner_id,
            hinge_side,
            position.cabinet_fixing_rows_mm,
            position.cabinet_center_mm,
            profile,
        )


__all__ = ["RiexNc70HardwareClearance"]
