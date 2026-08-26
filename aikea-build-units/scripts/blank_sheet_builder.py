"""Scope: Build one sheet blank in canonical local coordinates."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

Point2D = tuple[float, float]


@dataclass(frozen=True, slots=True)
class BlankSheetBuilder:
    """Extrude one calculated flat outline through its material thickness."""

    outline_mm: tuple[Point2D, ...]
    thickness_mm: float

    @classmethod
    def rectangle(
        cls,
        width_mm: float,
        height_mm: float,
        thickness_mm: float,
    ) -> "BlankSheetBuilder":
        """Describe a rectangular blank beginning at the local origin."""
        return cls(
            outline_mm=(
                (0.0, 0.0),
                (width_mm, 0.0),
                (width_mm, height_mm),
                (0.0, height_mm),
            ),
            thickness_mm=thickness_mm,
        )

    def build(self) -> cq.Workplane:
        """Return the outlined CadQuery blank with thickness along positive Z."""
        return (
            cq.Workplane("XY")
            .polyline(self.outline_mm)
            .close()
            .extrude(self.thickness_mm)
        )


__all__ = ["BlankSheetBuilder", "Point2D"]
