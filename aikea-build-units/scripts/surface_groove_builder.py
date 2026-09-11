"""Scope: Resolve one dimensioned surface groove through the common entry-face contract."""

from math import isfinite

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from part_construction_error import PartConstructionError
from surface_entry_validator import SurfaceEntryValidator


class SurfaceGrooveBuilder:
    def build(self, part, request):
        dimensions = (request.length_mm, request.width_mm, request.depth_mm)
        if any(not isfinite(value) or value <= 0 for value in dimensions):
            raise PartConstructionError(f"{request.machining_id}: groove dimensions must be finite and positive")
        length, width, depth = dimensions
        cutter = cq.Workplane('XY').box(length, width, depth, centered=(False, True, False)).val()
        opening = cq.Face.makeFromWires(cq.Wire.makePolygon([
            cq.Vector(x, y, 0) for x, y in ((0, -width/2), (length, -width/2),
                                           (length, width/2), (0, width/2), (0, -width/2))]))
        location = LocalToParentLocation().build(request.surface_to_part)
        SurfaceEntryValidator().require_on_surface(part, (("groove", opening),), location, request.machining_id)
        return cutter, location
