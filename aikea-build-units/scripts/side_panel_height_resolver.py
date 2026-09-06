"""Scope: Resolve side-panel heights from the top joint that each side supports."""

from __future__ import annotations

from math import isclose

from assembly_taxonomy import BoundaryPoint


class SidePanelHeightResolver:
    """Keep square tops bearing on sides while preserving angled miter material."""

    def resolve_left(
        self,
        top: tuple[BoundaryPoint, ...],
        top_thickness_mm: float,
    ) -> float:
        return self._resolve_end(top[0], top[1], top_thickness_mm)

    def resolve_right(
        self,
        top: tuple[BoundaryPoint, ...],
        top_thickness_mm: float,
    ) -> float:
        return self._resolve_end(top[-1], top[-2], top_thickness_mm)

    def _resolve_end(
        self,
        outside: BoundaryPoint,
        adjacent: BoundaryPoint,
        top_thickness_mm: float,
    ) -> float:
        if isclose(outside.height_mm, adjacent.height_mm):
            return outside.height_mm - top_thickness_mm
        return outside.height_mm


__all__ = ["SidePanelHeightResolver"]
