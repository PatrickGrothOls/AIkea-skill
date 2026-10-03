"""Scope: Build and place one Korrekt negative and its conservative plate footprint."""

from math import isfinite

import cadquery as cq

from korrekt_mounting_profile import KorrektMountingProfile
from part_construction_error import PartConstructionError
from surface_hole_pattern import SurfaceHole, SurfaceHolePattern


class KorrektMountingCutter:
    """Keep hole geometry and plate outline in the same native mounting frame."""

    def __init__(self) -> None:
        self.profile = KorrektMountingProfile()

    def cutout(self, panel_thickness_mm: float) -> cq.Shape:
        if not isfinite(panel_thickness_mm) or panel_thickness_mm <= 0:
            raise PartConstructionError("Korrekt cutter requires positive panel thickness")
        holes = tuple(SurfaceHole(f"mounting_{index}", x, -y, diameter, panel_thickness_mm+1)
                      for index, (x, y, diameter) in enumerate(self.profile.bores, 1))
        surface = cq.Plane(origin=(0, 0, panel_thickness_mm), xDir=(1, 0, 0), normal=(0, 0, -1))
        return cq.Compound.makeCompound([hole.cutter for hole in
            SurfaceHolePattern(holes).place(surface, entry_clearance_mm=1)])

    def footprint(self) -> cq.Wire:
        left, right, front, rear = self.profile.plate_bounds_xy_mm
        return cq.Workplane("XY").polyline(
            ((left, front), (right, front), (right, rear), (left, rear))
        ).close().val()

    def placement(self, axis_xy_mm: tuple[float, float], bottom_z_mm: float,
                  rotation_deg: float) -> cq.Location:
        values = (*axis_xy_mm, bottom_z_mm, rotation_deg)
        if not all(isfinite(value) for value in values):
            raise PartConstructionError("Korrekt placement must contain finite coordinates")
        sx, sy = self.profile.socket_axis_xy_mm
        return (cq.Location(cq.Vector(*axis_xy_mm, bottom_z_mm), cq.Vector(0, 0, 1), rotation_deg)
                * cq.Location(cq.Vector(-sx, -sy, 0)))
