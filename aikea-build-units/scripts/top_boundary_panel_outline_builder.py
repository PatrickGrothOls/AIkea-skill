"""Scope: Build a panel face outline from a clipped assembly top boundary."""

from __future__ import annotations

from assembly_taxonomy import BoundaryPoint


class TopBoundaryPanelOutlineBuilder:
    """Create a bottom-closed panel outline over any horizontal boundary span."""

    _TOLERANCE_MM = 1e-6

    def build(
        self,
        top: tuple[BoundaryPoint, ...],
        left_x_mm: float,
        right_x_mm: float,
        height_offset_mm: float = 0.0,
    ) -> tuple[BoundaryPoint, ...]:
        local_top = (
            BoundaryPoint(0.0, self._height_at(top, left_x_mm) + height_offset_mm),
            *(
                BoundaryPoint(
                    point.x_mm - left_x_mm,
                    point.height_mm + height_offset_mm,
                )
                for point in top
                if (
                    left_x_mm + self._TOLERANCE_MM
                    < point.x_mm
                    < right_x_mm - self._TOLERANCE_MM
                )
            ),
            BoundaryPoint(
                right_x_mm - left_x_mm,
                self._height_at(top, right_x_mm) + height_offset_mm,
            ),
        )
        return (
            BoundaryPoint(0.0, 0.0),
            BoundaryPoint(right_x_mm - left_x_mm, 0.0),
            *reversed(local_top),
        )

    def _height_at(
        self,
        top: tuple[BoundaryPoint, ...],
        x_mm: float,
    ) -> float:
        left, right = next(
            (left, right)
            for left, right in zip(top, top[1:])
            if (
                left.x_mm - self._TOLERANCE_MM
                <= x_mm
                <= right.x_mm + self._TOLERANCE_MM
            )
        )
        span_mm = right.x_mm - left.x_mm
        progress = 0.0 if span_mm == 0 else (x_mm - left.x_mm) / span_mm
        progress = min(1.0, max(0.0, progress))
        return left.height_mm + progress * (right.height_mm - left.height_mm)


__all__ = ["TopBoundaryPanelOutlineBuilder"]
