"""Scope: Calculate where vertical carcass panels meet the top-panel underside."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isclose

from assembly_taxonomy import BoundaryPoint


@dataclass(frozen=True)
class _BoundaryLine:
    """Represent one top segment after shifting it below the outside surface."""

    slope: float
    intercept: float

    def height_at(self, x_mm: float) -> float:
        return self.slope * x_mm + self.intercept


class TopPanelUndersideBoundary:
    """Offset the outside top profile by the sheet thickness along its normal."""

    def build(
        self,
        outside: tuple[BoundaryPoint, ...],
        thickness_mm: float,
    ) -> tuple[BoundaryPoint, ...]:
        lines = tuple(
            self._offset_line(left, right, thickness_mm)
            for left, right in zip(outside, outside[1:])
        )
        inside = [BoundaryPoint(outside[0].x_mm, lines[0].height_at(outside[0].x_mm))]
        inside.extend(
            self._intersection(left, right, outside[index].x_mm)
            for index, (left, right) in enumerate(zip(lines, lines[1:]), start=1)
        )
        inside.append(
            BoundaryPoint(outside[-1].x_mm, lines[-1].height_at(outside[-1].x_mm))
        )
        return tuple(inside)

    def _offset_line(
        self,
        left: BoundaryPoint,
        right: BoundaryPoint,
        thickness_mm: float,
    ) -> _BoundaryLine:
        run_mm = right.x_mm - left.x_mm
        rise_mm = right.height_mm - left.height_mm
        slope = rise_mm / run_mm
        outside_intercept = left.height_mm - slope * left.x_mm
        vertical_offset_mm = thickness_mm * hypot(run_mm, rise_mm) / run_mm
        return _BoundaryLine(slope, outside_intercept - vertical_offset_mm)

    def _intersection(
        self,
        left: _BoundaryLine,
        right: _BoundaryLine,
        fallback_x_mm: float,
    ) -> BoundaryPoint:
        if isclose(left.slope, right.slope):
            return BoundaryPoint(fallback_x_mm, left.height_at(fallback_x_mm))
        x_mm = (right.intercept - left.intercept) / (left.slope - right.slope)
        return BoundaryPoint(x_mm, left.height_at(x_mm))


__all__ = ["TopPanelUndersideBoundary"]
