"""Scope: Validate a drilling entry face and place its dimensioned cutter in a panel."""

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from panel_blank_builder import PanelBlankBuilder
from part_construction_error import PartConstructionError
from surface_hole_pattern import SurfaceHolePattern


class SurfaceDrillingBuilder:
    """Reject sealed internal cavities while allowing any actual planar entry face."""

    def build(self, part, request):
        pattern = SurfaceHolePattern(request.holes)
        location = LocalToParentLocation().build(request.surface_to_part)
        faces = cq.Compound.makeCompound(PanelBlankBuilder().build(part).val().Faces())
        for hole in pattern.holes:
            entry = cq.Face.makeFromWires(cq.Wire.makeCircle(
                hole.diameter_mm / 2, cq.Vector(hole.x_mm, hole.y_mm, 0), cq.Vector(0, 0, 1),
            )).located(location)
            if entry.cut(faces).Area() > 1e-6:
                raise PartConstructionError(f"{request.machining_id}/{hole.hole_id}: drilling must start on an entry face")
        holes = pattern.place(cq.Plane.XY(), entry_clearance_mm=0)
        cutter = holes[0].cutter
        for hole in holes[1:]:
            cutter = cutter.fuse(hole.cutter)
        return cutter, location
