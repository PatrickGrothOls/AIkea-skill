"""Scope: Derive adjustable shelf parts from one cabinet's valid support-hole rows."""

from __future__ import annotations

from dataclasses import dataclass

from assembly_taxonomy import AssemblyTaxonomyInputError, PartTaxonomy
from system_32_side_panel_grid import (
    System32SidePanelGrid,
    System32SidePanelGridProfile,
)


@dataclass(frozen=True)
class AdjustableShelfProfile:
    """Define the supplied shelf count without making it a room-wide setting."""

    shelf_count: int = 3


class AdjustableShelfTaxonomyBuilder:
    """Create shelf panels supported by rows shared by both cabinet sides."""

    def __init__(
        self,
        profile: AdjustableShelfProfile | None = None,
        grid_profile: System32SidePanelGridProfile | None = None,
    ) -> None:
        self.profile = profile or AdjustableShelfProfile()
        self.hardware_grid = System32SidePanelGrid(grid_profile)

    def build(
        self,
        width_mm: float,
        depth_mm: float,
        left_side_height_mm: float,
        right_side_height_mm: float,
        thickness_mm: float,
    ) -> tuple[PartTaxonomy, ...]:
        shelf_width_mm = width_mm - (2.0 * thickness_mm)
        shared_rows = self.hardware_grid.row_heights_mm(
            min(left_side_height_mm, right_side_height_mm)
        )
        selected_rows = self._select_even_rows(shared_rows)
        support_offset_mm = self.hardware_grid.profile.hole_diameter_mm / 2.0
        return tuple(
            PartTaxonomy(
                part_id=f"shelf_{number:02d}",
                role="shelf_panel",
                dimensions_mm=(
                    ("width", shelf_width_mm),
                    ("depth", depth_mm),
                    ("thickness", thickness_mm),
                    ("assembly_x", thickness_mm),
                    ("assembly_y", 0.0),
                    ("support_row_height", row_height_mm),
                    ("bottom_height", row_height_mm + support_offset_mm),
                ),
                local_size_mm=(shelf_width_mm, depth_mm, thickness_mm),
            )
            for number, row_height_mm in enumerate(selected_rows, start=1)
        )

    def _select_even_rows(self, rows: tuple[float, ...]) -> tuple[float, ...]:
        count = self.profile.shelf_count
        if count < 1 or len(rows) < count:
            raise AssemblyTaxonomyInputError(
                [f"tall storage requires at least {count} shared shelf-support rows"]
            )
        row_count = len(rows)
        return tuple(rows[(number * row_count) // (count + 1)] for number in range(1, count + 1))


__all__ = ["AdjustableShelfProfile", "AdjustableShelfTaxonomyBuilder"]
