"""Scope: Resolve only exact whole-hole reuse from named prior local operations."""

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from part_construction_error import PartConstructionError
from surface_hole_pattern import SurfaceHolePattern


class SurfaceDrillingReuse:
    TOLERANCE_MM3 = 1e-5

    def resolve(self, request, preceding, local_ids):
        references = getattr(request, "reuse_machining_ids", ())
        if not references:
            return None
        if request.operation_type != "surface_holes" or len(set(references)) != len(references):
            raise PartConstructionError(f"{request.machining_id}: invalid drilling reuse declaration")
        prior = {cut.joint_id: cut for cut in preceding
                 if cut.part_id == request.part_id and cut.joint_id in local_ids}
        if any(identity not in prior for identity in references):
            raise PartConstructionError(f"{request.machining_id}: reuse requires earlier local machining on the same part")
        holes = self._holes(request)
        reused = set()
        for identity in references:
            matches = self._matches(holes, prior[identity])
            if not matches:
                raise PartConstructionError(f"{request.machining_id}: {identity} has no exactly matching whole hole")
            reused.update(matches)
        return cq.Compound.makeCompound([holes[index] for index in sorted(reused)])

    def matching_operations(self, request, prior_local_cuts):
        """Let recipes save discovered exact sources as explicit editable dependencies."""
        holes = self._holes(request)
        return tuple(dict.fromkeys(cut.joint_id for cut in prior_local_cuts
                                   if cut.part_id == request.part_id and self._matches(holes, cut)))

    def _holes(self, request):
        location = LocalToParentLocation().build(request.surface_to_part)
        return tuple(hole.cutter.located(location) for hole in
                     SurfaceHolePattern(request.holes).place(cq.Plane.XY(), entry_clearance_mm=0))

    def _matches(self, holes, cut):
        source = cut.cutter.located(cut.location)
        return {index for index, hole in enumerate(holes)
                if any(self._equal(hole, solid) for solid in source.Solids())}

    def _equal(self, hole, source):
        left, right = hole.BoundingBox(), source.BoundingBox()
        if any(abs(getattr(left, axis) - getattr(right, axis)) > 1e-6
               for axis in ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax")):
            return False
        return hole.cut(source).Volume() + source.cut(hole).Volume() <= self.TOLERANCE_MM3
