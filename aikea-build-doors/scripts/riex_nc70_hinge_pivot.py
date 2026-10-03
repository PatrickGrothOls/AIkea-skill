"""Scope: Resolve the verified Riex NC70 opening axis without CAD dependencies."""

from __future__ import annotations

from typing import Any

from door_hinge_side import DoorHingeSide
from door_host import DoorHost
from riex_nc70_hinge_profile import RiexNc70HingeProfile


class RiexNc70HingePivot:
    """Map the source hinge axis to either cabinet edge by rigid rotation."""

    def resolve(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide,
    ) -> tuple[float, float]:
        origin_x_mm = self.hinge_origin_x(assembly, profile, hinge_side)
        pivot_offset_mm = profile.native_pivot_y_mm
        pivot_x_mm = (
            origin_x_mm - pivot_offset_mm
            if hinge_side is DoorHingeSide.LEFT
            else origin_x_mm + pivot_offset_mm
        )
        host = DoorHost.resolve(assembly, hinge_side)
        pivot_y_mm = host.front_mm-profile.native_door_surface_x_mm + profile.native_pivot_x_mm
        return pivot_x_mm, pivot_y_mm

    def hinge_origin_x(
        self,
        assembly: Any,
        profile: RiexNc70HingeProfile,
        hinge_side: DoorHingeSide,
    ) -> float:
        host = DoorHost.resolve(assembly, hinge_side)
        offset = profile.source_origin_from_door_edge_mm
        return host.door_edge_x_mm + (offset if hinge_side is DoorHingeSide.LEFT else -offset)


__all__ = ["RiexNc70HingePivot"]
