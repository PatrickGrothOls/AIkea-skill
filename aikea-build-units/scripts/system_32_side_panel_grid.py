"""Scope: Calculate and machine one side panel's shared System 32 hardware grid."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from part_construction_error import PartConstructionError


@dataclass(frozen=True, slots=True)
class System32SidePanelGridProfile:
    """Hold the cabinet-owned grid dimensions outside project-wide settings."""

    grid_id: str = "system-32-side-panel-v1"
    hole_diameter_mm: float = 5.0
    row_pitch_mm: float = 32.0
    first_row_height_mm: float = 100.0
    top_clearance_mm: float = 100.0
    front_rear_setback_mm: float = 37.0
    hole_depth_mm: float = 13.0


class System32SidePanelGrid:
    """Provide one bottom-aligned grid to every compatible cabinet fitting."""

    def __init__(self, profile: System32SidePanelGridProfile | None = None) -> None:
        self.profile = profile or System32SidePanelGridProfile()

    def row_heights_mm(self, panel_height_mm: float) -> tuple[float, ...]:
        usable_top_mm = panel_height_mm - self.profile.top_clearance_mm
        rows: list[float] = []
        row_mm = self.profile.first_row_height_mm
        while row_mm <= usable_top_mm + 1e-6:
            rows.append(row_mm)
            row_mm += self.profile.row_pitch_mm
        return tuple(rows)

    def adjacent_row_pairs_mm(
        self,
        panel_height_mm: float,
    ) -> tuple[tuple[float, float], ...]:
        rows = self.row_heights_mm(panel_height_mm)
        return tuple(zip(rows, rows[1:]))

    def rows_nearest_mm(
        self,
        panel_height_mm: float,
        requested_height_mm: float,
    ) -> tuple[float, ...]:
        """Order valid rows by proximity while keeping lower rows deterministic."""
        return tuple(
            sorted(
                self.row_heights_mm(panel_height_mm),
                key=lambda row_mm: (abs(row_mm - requested_height_mm), row_mm),
            )
        )

    def column_positions_mm(self, panel_depth_mm: float) -> tuple[float, float]:
        setback_mm = self.profile.front_rear_setback_mm
        if panel_depth_mm <= 2.0 * setback_mm:
            raise PartConstructionError(
                "System 32 grid requires separate front and rear columns"
            )
        return setback_mm, panel_depth_mm - setback_mm

    def apply(self, part: Any, workpiece: Any) -> Any:
        import cadquery as cq

        dimensions = {name: float(value) for name, value in part.dimensions_mm}
        thickness_mm = dimensions["thickness"]
        if self.profile.hole_depth_mm >= thickness_mm:
            raise PartConstructionError(
                f"System 32 grid requires more than {self.profile.hole_depth_mm:g} mm thickness"
            )
        z_start_by_face = {
            ">Z": thickness_mm - self.profile.hole_depth_mm,
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
            .circle(self.profile.hole_diameter_mm / 2.0)
            .extrude(self.profile.hole_depth_mm)
            .translate((0.0, 0.0, z_start_by_face[part.inside_face]))
        )
        return workpiece.cut(cutter)


__all__ = ["System32SidePanelGrid", "System32SidePanelGridProfile"]
