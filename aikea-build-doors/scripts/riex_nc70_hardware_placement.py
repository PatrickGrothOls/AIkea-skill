"""Scope: Place exact Riex NC70 source CAD in one cabinet-local frame."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from door_hinge_plan import DoorHingePlan
from door_hinge_side import DoorHingeSide
from riex_nc70_hardware_frame import (
    RiexNc70HardwareFrame,
    RiexNc70HardwareFrameResolver,
)
from riex_nc70_hardware_loader import RiexNc70HardwareSet
from riex_nc70_hinge_profile import RiexNc70HingeProfile
from unit_mockup import MockupPart


class RiexNc70HardwarePlacement:
    """Map unchanged manufacturer frames into one fitted cabinet."""

    _METAL = (0.48, 0.50, 0.52, 1.0)

    def __init__(self) -> None:
        self.frames = RiexNc70HardwareFrameResolver()

    def parts(
        self,
        assembly: Any,
        hardware: RiexNc70HardwareSet,
        plan: DoorHingePlan,
        profile: RiexNc70HingeProfile,
        opened: bool,
    ) -> tuple[MockupPart, ...]:
        hinge_shape = hardware.open_hinge if opened else hardware.closed_hinge
        parts = []
        for placement in plan.placements:
            hinge_location = self.hinge_location(
                assembly,
                profile,
                float(assembly.door_bottom_mm) + placement.door_height_mm,
                plan.hinge_side,
            )
            plate_location = self.plate_location(
                assembly,
                profile,
                float(assembly.base_height_mm) + placement.cabinet_height_mm,
                plan.hinge_side,
            )
            parts.extend(
                (
                    MockupPart(
                        f"{placement.hinge_id}__source_cad",
                        cq.Workplane(obj=hinge_shape),
                        hinge_location,
                        self._METAL,
                    ),
                    MockupPart(
                        f"{placement.hinge_id}_plate__source_cad",
                        cq.Workplane(obj=hardware.mounting_plate),
                        plate_location,
                        self._METAL,
                    ),
                )
            )
        return tuple(parts)

    def hinge_location(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        center_z_mm: float,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
    ) -> cq.Location:
        return self._location(
            self.frames.hinge(assembly, profile, center_z_mm, hinge_side)
        )

    def plate_location(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        center_z_mm: float,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
    ) -> cq.Location:
        return self._location(
            self.frames.plate(assembly, profile, center_z_mm, hinge_side)
        )

    def _location(self, frame: RiexNc70HardwareFrame) -> cq.Location:
        return cq.Location(
            cq.Plane(
                origin=frame.origin_mm,
                xDir=frame.local_x_in_cabinet,
                normal=frame.local_z_in_cabinet,
            )
        )

    def pivot(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
    ) -> tuple[float, float]:
        return self.frames.pivot(assembly, profile, hinge_side)


__all__ = ["RiexNc70HardwarePlacement"]
