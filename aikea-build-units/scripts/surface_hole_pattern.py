"""Scope: Place dimensioned drilling patterns on explicit planar surface datums."""

from dataclasses import dataclass
from math import isfinite
import cadquery as cq


@dataclass(frozen=True)
class SurfaceHole:
    hole_id: str
    x_mm: float
    y_mm: float
    diameter_mm: float
    depth_mm: float

    def __post_init__(self):
        values = (self.x_mm, self.y_mm, self.diameter_mm, self.depth_mm)
        if not all(isfinite(value) for value in values) or min(values[2:]) <= 0:
            raise ValueError("hole coordinates must be finite and diameter/depth positive")


@dataclass(frozen=True)
class PlacedSurfaceHole:
    spec: SurfaceHole
    cutter: cq.Shape


class SurfaceHolePattern:
    def __init__(self, holes: tuple[SurfaceHole, ...]):
        identifiers = tuple(hole.hole_id for hole in holes)
        if not identifiers or len(set(identifiers)) != len(identifiers):
            raise ValueError("a drilling pattern requires distinct hole IDs")
        self.holes = holes

    def place(self, surface: cq.Plane, entry_clearance_mm=0.1):
        """Place cutters with local +Z into material and depth measured from the datum."""
        if not isfinite(entry_clearance_mm) or entry_clearance_mm < 0:
            raise ValueError("entry clearance must be finite and nonnegative")
        return tuple(PlacedSurfaceHole(hole,
            cq.Workplane(surface).workplane(offset=-entry_clearance_mm)
            .center(hole.x_mm, hole.y_mm).circle(hole.diameter_mm/2)
            .extrude(hole.depth_mm+entry_clearance_mm).val()) for hole in self.holes)
