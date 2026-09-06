"""Scope: Derive local top-panel specifications from one assembly boundary."""

from __future__ import annotations

from math import hypot

from assembly_taxonomy import BoundaryPoint, PartTaxonomy


class TopPanelTaxonomyBuilder:
    """Preserve every measured top segment across the full assembly width."""

    def build(
        self,
        top: tuple[BoundaryPoint, ...],
        depth_mm: float,
        thickness_mm: float,
    ) -> tuple[PartTaxonomy, ...]:
        return tuple(
            self._segment(
                index,
                left,
                right,
                depth_mm,
                thickness_mm,
            )
            for index, (left, right) in enumerate(zip(top, top[1:]))
        )

    def _segment(
        self,
        index: int,
        left: BoundaryPoint,
        right: BoundaryPoint,
        depth_mm: float,
        thickness_mm: float,
    ) -> PartTaxonomy:
        start_x_mm = left.x_mm
        end_x_mm = right.x_mm
        start_height_mm = left.height_mm
        end_height_mm = right.height_mm
        length_mm = hypot(
            end_x_mm - start_x_mm,
            end_height_mm - start_height_mm,
        )
        dimensions = (
            ("start_x", start_x_mm),
            ("end_x", end_x_mm),
            ("start_height", start_height_mm),
            ("end_height", end_height_mm),
            ("length", length_mm),
            ("depth", depth_mm),
            ("thickness", thickness_mm),
        )
        return PartTaxonomy(
            f"top_panel_{index + 1:02d}",
            "top_panel",
            dimensions,
            local_size_mm=(length_mm, depth_mm, thickness_mm),
            inside_face="<Z",
        )

__all__ = ["TopPanelTaxonomyBuilder"]
