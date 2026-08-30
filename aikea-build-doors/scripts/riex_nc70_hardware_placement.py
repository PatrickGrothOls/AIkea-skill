"""Scope: Place exact Riex NC70 source CAD in one cabinet-local frame."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from door_hinge_plan import DoorHingePlan
from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_pivot import RiexNc70HingePivot
from riex_nc70_hardware_loader import RiexNc70HardwareSet
from riex_nc70_hinge_profile import RiexNc70HingeProfile
from unit_mockup import MockupPart


class RiexNc70HardwarePlacement:
    """Map unchanged manufacturer frames into one fitted cabinet."""

    _METAL = (0.48, 0.50, 0.52, 1.0)

    def __init__(self) -> None:
        self.hinge_pivot = RiexNc70HingePivot()

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
        origin_x_mm = self.hinge_pivot.hinge_origin_x(
            assembly, profile, hinge_side
        )
        return cq.Location(
            cq.Plane(
                origin=(
                    origin_x_mm,
                    -profile.native_door_surface_x_mm,
                    center_z_mm,
                ),
                xDir=(0.0, 1.0, 0.0),
                normal=(
                    (0.0, 0.0, 1.0)
                    if hinge_side is DoorHingeSide.LEFT
                    else (0.0, 0.0, -1.0)
                ),
            )
        )

    def plate_location(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        center_z_mm: float,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
    ) -> cq.Location:
        side_thickness_mm = self._dimensions(assembly.part(hinge_side.side_part_id))[
            "thickness"
        ]
        origin_x_mm = side_thickness_mm + profile.plate_native_panel_face_y_mm
        origin_z_mm = center_z_mm - profile.plate_native_vertical_center_x_mm
        x_direction = (0.0, 0.0, 1.0)
        if hinge_side is DoorHingeSide.RIGHT:
            origin_x_mm = float(assembly.width_mm) - origin_x_mm
            origin_z_mm = center_z_mm + profile.plate_native_vertical_center_x_mm
            x_direction = (0.0, 0.0, -1.0)
        return cq.Location(
            cq.Plane(
                origin=(
                    origin_x_mm,
                    profile.plate_line_from_front_mm
                    + profile.plate_native_fixing_axis_z_mm,
                    origin_z_mm,
                ),
                xDir=x_direction,
                normal=(0.0, -1.0, 0.0),
            )
        )

    def pivot(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide = DoorHingeSide.LEFT,
    ) -> tuple[float, float]:
        return self.hinge_pivot.resolve(assembly, profile, hinge_side)

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["RiexNc70HardwarePlacement"]
