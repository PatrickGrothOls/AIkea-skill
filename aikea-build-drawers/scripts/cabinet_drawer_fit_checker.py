"""Scope: Reject one resolved drawer layout that cannot fit its cabinet bay."""

from __future__ import annotations

from typing import Any
from drawer_host import DrawerHost

Vector3D = tuple[float, float, float]


class CabinetDrawerFitChecker:
    """Check the planned box, runner depth, and vertical cabinet opening."""

    def require_fit(
        self,
        cabinet: Any,
        box: Any,
        required_inside_depth_mm: float,
        origin: Vector3D,
    ) -> None:
        host = DrawerHost.resolve(cabinet)
        space = host.spec
        boundaries = (
            origin[0] >= host.inside_x("left"),
            origin[0] + box.outside_width_mm <= host.inside_x("right"),
            required_inside_depth_mm <= space.inside_depth_mm,
            origin[1] >= space.front_mm,
            origin[1] + box.outside_depth_mm <= space.front_mm + space.inside_depth_mm,
            origin[2] >= space.bottom_mm,
            origin[2] + box.sizing.box_height_mm <= space.top_mm,
        )
        if not all(boundaries):
            raise ValueError("drawer layout does not fit inside the selected cabinet bay")


__all__ = ["CabinetDrawerFitChecker", "Vector3D"]
