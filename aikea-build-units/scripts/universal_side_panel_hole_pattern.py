"""Scope: Apply the reusable shelf-and-hanger hardware holes to one side panel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from part_construction_error import PartConstructionError


@dataclass(frozen=True)
class UniversalSidePanelHoleProfile:
    """Hold the proven blind-hole dimensions outside project-wide settings."""

    diameter_mm: float = 5.0
    spacing_mm: float = 64.0
    top_clearance_mm: float = 100.0
    bottom_clearance_mm: float = 100.0
    depth_mm: float = 13.0


class UniversalSidePanelHolePattern:
    """Machine bottom-aligned front and back columns into a side panel."""

    def __init__(self, profile: UniversalSidePanelHoleProfile | None = None) -> None:
        self.profile = profile or UniversalSidePanelHoleProfile()

    def row_heights_mm(self, panel_height_mm: float) -> tuple[float, ...]:
        usable_top_mm = panel_height_mm - self.profile.top_clearance_mm
        row_heights: list[float] = []
        height_mm = self.profile.bottom_clearance_mm
        while height_mm <= usable_top_mm + 1e-6:
            row_heights.append(height_mm)
            height_mm += self.profile.spacing_mm
        return tuple(row_heights)

    def column_positions_mm(self, panel_depth_mm: float) -> tuple[float, float]:
        edge_distance_mm = panel_depth_mm / 4.0
        return edge_distance_mm, panel_depth_mm - edge_distance_mm

    def apply(self, part: Any, workpiece: Any) -> Any:
        import cadquery as cq

        dimensions = {name: float(value) for name, value in part.dimensions_mm}
        thickness_mm = dimensions["thickness"]
        if self.profile.depth_mm >= thickness_mm:
            raise PartConstructionError(
                f"universal side-panel holes require more than {self.profile.depth_mm:g} mm thickness"
            )
        z_start_by_face = {
            ">Z": thickness_mm - self.profile.depth_mm,
            "<Z": 0.0,
        }
        if part.inside_face not in z_start_by_face:
            raise PartConstructionError(
                f"unsupported side-panel inside face: {part.inside_face}"
            )
        points = tuple(
            (column_mm, row_mm)
            for row_mm in self.row_heights_mm(dimensions["height"])
            for column_mm in self.column_positions_mm(dimensions["depth"])
        )
        cutter = (
            cq.Workplane("XY")
            .pushPoints(points)
            .circle(self.profile.diameter_mm / 2.0)
            .extrude(self.profile.depth_mm)
            .translate((0.0, 0.0, z_start_by_face[part.inside_face]))
        )
        return workpiece.cut(cutter)


__all__ = ["UniversalSidePanelHolePattern", "UniversalSidePanelHoleProfile"]
