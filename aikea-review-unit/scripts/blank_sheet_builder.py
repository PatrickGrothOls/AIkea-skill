"""Scope: Build one rectangular sheet blank in canonical local coordinates."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True, slots=True)
class BlankSheetBuilder:
    """Create an unmachined sheet face in XY with thickness along positive Z."""

    width_mm: float
    height_mm: float
    thickness_mm: float

    def build(self) -> cq.Workplane:
        """Return the rectangular CadQuery blank anchored at the local origin."""
        return (
            cq.Workplane("XY")
            .rect(self.width_mm, self.height_mm, centered=False)
            .extrude(self.thickness_mm)
        )


__all__ = ["BlankSheetBuilder"]
