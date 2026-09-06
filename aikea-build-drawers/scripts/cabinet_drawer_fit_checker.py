"""Scope: Reject one resolved drawer layout that cannot fit its cabinet bay."""

from __future__ import annotations

from typing import Any

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
        left_mm = float(cabinet.part("left_side").local_size_mm[2])
        right_mm = (
            float(cabinet.width_mm)
            - float(cabinet.part("right_side").local_size_mm[2])
        )
        shelf_bottoms = (
            float(dict(part.dimensions_mm)["bottom_height"])
            for part in cabinet.parts
            if part.role == "shelf_panel"
        )
        inside_top_mm = float(cabinet.base_height_mm) + min(
            shelf_bottoms,
            default=min(point.height_mm for point in cabinet.top),
        )
        boundaries = (
            origin[0] >= left_mm,
            origin[0] + box.outside_width_mm <= right_mm,
            required_inside_depth_mm <= float(cabinet.inside_depth_mm),
            origin[1] + box.outside_depth_mm <= float(cabinet.inside_depth_mm),
            origin[2] >= float(cabinet.base_height_mm),
            origin[2] + box.sizing.box_height_mm <= inside_top_mm,
        )
        if not all(boundaries):
            raise ValueError("drawer layout does not fit inside the selected cabinet bay")


__all__ = ["CabinetDrawerFitChecker", "Vector3D"]
