"""Scope: Measure axis-aligned bounds of parts already placed in an assembly."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class PlacedBounds:
    """Carry one measured XYZ extent through local and project coordinates."""

    x_min_mm: float
    x_max_mm: float
    y_min_mm: float
    y_max_mm: float
    z_min_mm: float
    z_max_mm: float

    @classmethod
    def from_parts(cls, parts: Iterable[Any]) -> "PlacedBounds":
        measured = tuple(part.placed_shape().BoundingBox() for part in parts)
        return cls(
            min(bound.xmin for bound in measured),
            max(bound.xmax for bound in measured),
            min(bound.ymin for bound in measured),
            max(bound.ymax for bound in measured),
            min(bound.zmin for bound in measured),
            max(bound.zmax for bound in measured),
        )

    def shifted(self, offset_mm: tuple[float, float, float]) -> "PlacedBounds":
        x_mm, y_mm, z_mm = offset_mm
        return PlacedBounds(
            self.x_min_mm + x_mm,
            self.x_max_mm + x_mm,
            self.y_min_mm + y_mm,
            self.y_max_mm + y_mm,
            self.z_min_mm + z_mm,
            self.z_max_mm + z_mm,
        )

    def as_dict(self) -> dict[str, list[float]]:
        return {
            "minimum_mm": [self.x_min_mm, self.y_min_mm, self.z_min_mm],
            "maximum_mm": [self.x_max_mm, self.y_max_mm, self.z_max_mm],
        }

    def covers_xy(self, other: "PlacedBounds", tolerance_mm: float) -> bool:
        return (
            self.x_min_mm <= other.x_min_mm + tolerance_mm
            and self.x_max_mm >= other.x_max_mm - tolerance_mm
            and self.y_min_mm <= other.y_min_mm + tolerance_mm
            and self.y_max_mm >= other.y_max_mm - tolerance_mm
        )

    def matches_x_span(
        self,
        start_x_mm: float,
        end_x_mm: float,
        tolerance_mm: float,
    ) -> bool:
        return (
            abs(self.x_min_mm - start_x_mm) <= tolerance_mm
            and abs(self.x_max_mm - end_x_mm) <= tolerance_mm
        )


__all__ = ["PlacedBounds"]
