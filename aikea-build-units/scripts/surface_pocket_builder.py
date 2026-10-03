"""Scope: Shape a rounded pocket while reusing common surface-entry and dimension checks."""
from math import isfinite
import cadquery as cq
from part_construction_error import PartConstructionError
from surface_groove_builder import SurfaceGrooveBuilder


class SurfacePocketBuilder(SurfaceGrooveBuilder):
    def _cutter(self, dimensions, request):
        radius = request.corner_radius_mm
        if not isfinite(radius) or not 0 <= radius < min(dimensions[:2])/2:
            raise PartConstructionError(f"{request.machining_id}: pocket radius must fit inside its opening")
        cutter = super()._cutter(dimensions, request)
        return cq.Workplane(obj=cutter).edges('|Z').fillet(radius).val() if radius else cutter
