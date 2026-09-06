"""Scope: Map exact Riex NC70 mounting plates onto shared cabinet hardware space."""

from __future__ import annotations

from typing import Any

from door_hinge_side import DoorHingeSide
from panel_hardware_reservation import PanelHardwareReservation
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class RiexNc70HardwareReservations:
    """Reserve both plate fixing nodes and the exact source-CAD envelope."""

    def from_plan(
        self,
        plan: Any,
        profile: RiexNc70HingeProfile,
    ) -> tuple[PanelHardwareReservation, ...]:
        return tuple(
            self.for_position(
                placement.hinge_id,
                plan.hinge_side,
                placement.cabinet_fixing_rows_mm,
                placement.cabinet_height_mm,
                profile,
            )
            for placement in plan.placements
        )

    def for_position(
        self,
        owner_id: str,
        hinge_side: DoorHingeSide,
        fixing_rows_mm: tuple[float, float],
        center_height_mm: float,
        profile: RiexNc70HingeProfile,
    ) -> PanelHardwareReservation:
        low_offset_mm, high_offset_mm = (
            profile.plate_height_interval_from_center_mm
        )
        return PanelHardwareReservation(
            owner_id=owner_id,
            hardware_kind="hinge_plate",
            side_part_id=hinge_side.side_part_id,
            system_32_node_rows_mm=fixing_rows_mm,
            depth_interval_mm=profile.plate_depth_interval_from_front_mm,
            height_interval_mm=(
                center_height_mm + low_offset_mm,
                center_height_mm + high_offset_mm,
            ),
        )


__all__ = ["RiexNc70HardwareReservations"]
