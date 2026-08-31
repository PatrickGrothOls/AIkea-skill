"""Scope: Resolve exact Riex NC70 hardware frames without geometry concerns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from door_hinge_side import DoorHingeSide
from riex_nc70_hinge_pivot import RiexNc70HingePivot
from riex_nc70_hinge_profile import RiexNc70HingeProfile

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class RiexNc70HardwareFrame:
    """Place unchanged manufacturer CAD inside a cabinet-local frame."""

    origin_mm: Vector3D
    local_x_in_cabinet: Vector3D
    local_y_in_cabinet: Vector3D
    local_z_in_cabinet: Vector3D


class RiexNc70HardwareFrameResolver:
    """Calculate the frames shared by builders, reviews, and tree traversal."""

    def __init__(self) -> None:
        self.hinge_pivot = RiexNc70HingePivot()

    def hinge(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        center_z_mm: float,
        hinge_side: DoorHingeSide,
    ) -> RiexNc70HardwareFrame:
        origin_x_mm = self.hinge_pivot.hinge_origin_x(
            assembly, profile, hinge_side
        )
        local_z = (
            (0.0, 0.0, 1.0)
            if hinge_side is DoorHingeSide.LEFT
            else (0.0, 0.0, -1.0)
        )
        return self._from_plane(
            (origin_x_mm, -profile.native_door_surface_x_mm, center_z_mm),
            (0.0, 1.0, 0.0),
            local_z,
        )

    def plate(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        center_z_mm: float,
        hinge_side: DoorHingeSide,
    ) -> RiexNc70HardwareFrame:
        side_thickness_mm = self._dimensions(
            assembly.part(hinge_side.side_part_id)
        )["thickness"]
        origin_x_mm = side_thickness_mm + profile.plate_native_panel_face_y_mm
        origin_z_mm = center_z_mm - profile.plate_native_vertical_center_x_mm
        local_x = (0.0, 0.0, 1.0)
        if hinge_side is DoorHingeSide.RIGHT:
            origin_x_mm = float(assembly.width_mm) - origin_x_mm
            origin_z_mm = center_z_mm + profile.plate_native_vertical_center_x_mm
            local_x = (0.0, 0.0, -1.0)
        return self._from_plane(
            (
                origin_x_mm,
                profile.plate_line_from_front_mm
                + profile.plate_native_fixing_axis_z_mm,
                origin_z_mm,
            ),
            local_x,
            (0.0, -1.0, 0.0),
        )

    def pivot(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide,
    ) -> tuple[float, float]:
        return self.hinge_pivot.resolve(assembly, profile, hinge_side)

    def _from_plane(
        self,
        origin: Vector3D,
        local_x: Vector3D,
        local_z: Vector3D,
    ) -> RiexNc70HardwareFrame:
        x_x, x_y, x_z = local_x
        z_x, z_y, z_z = local_z
        local_y = (
            (z_y * x_z) - (z_z * x_y),
            (z_z * x_x) - (z_x * x_z),
            (z_x * x_y) - (z_y * x_x),
        )
        return RiexNc70HardwareFrame(origin, local_x, local_y, local_z)

    def _dimensions(self, part: Any) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["RiexNc70HardwareFrame", "RiexNc70HardwareFrameResolver"]
