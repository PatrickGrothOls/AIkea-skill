"""Scope: Derive local top-panel specifications from one assembly boundary."""

from __future__ import annotations

from math import hypot, isclose

from assembly_taxonomy import BoundaryPoint, PartTaxonomy


class TopPanelTaxonomyBuilder:
    """Fit square top ends between sides while preserving miter boundaries."""

    def build(
        self,
        top: tuple[BoundaryPoint, ...],
        depth_mm: float,
        thickness_mm: float,
    ) -> tuple[PartTaxonomy, ...]:
        last_index = len(top) - 2
        return tuple(
            self._segment(
                index,
                left,
                right,
                depth_mm,
                thickness_mm,
                index == 0,
                index == last_index,
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
        is_first: bool,
        is_last: bool,
    ) -> PartTaxonomy:
        is_square_end = isclose(left.height_mm, right.height_mm)
        start_x_mm = left.x_mm + (thickness_mm if is_first and is_square_end else 0.0)
        end_x_mm = right.x_mm - (thickness_mm if is_last and is_square_end else 0.0)
        start_height_mm = self._height_at(left, right, start_x_mm)
        end_height_mm = self._height_at(left, right, end_x_mm)
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

    def _height_at(
        self,
        left: BoundaryPoint,
        right: BoundaryPoint,
        x_mm: float,
    ) -> float:
        proportion = (x_mm - left.x_mm) / (right.x_mm - left.x_mm)
        return left.height_mm + proportion * (right.height_mm - left.height_mm)


__all__ = ["TopPanelTaxonomyBuilder"]
