"""Scope: Validate a drilling entry face and place its dimensioned cutter in a panel."""

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from surface_entry_validator import SurfaceEntryValidator
from surface_hole_pattern import SurfaceHolePattern


class SurfaceDrillingBuilder:
    """Reject sealed internal cavities while allowing any actual planar entry face."""

    def build(self, part, request):
        pattern = SurfaceHolePattern(request.holes)
        location = LocalToParentLocation().build(request.surface_to_part)
        entries = tuple((hole.hole_id, cq.Face.makeFromWires(cq.Wire.makeCircle(
            hole.diameter_mm / 2, cq.Vector(hole.x_mm, hole.y_mm, 0), cq.Vector(0, 0, 1),
        ))) for hole in pattern.holes)
        SurfaceEntryValidator().require_on_surface(part, entries, location, request.machining_id)
        holes = pattern.place(cq.Plane.XY(), entry_clearance_mm=0)
        cutter = holes[0].cutter
        for hole in holes[1:]:
            cutter = cutter.fuse(hole.cutter)
        return cutter, location
