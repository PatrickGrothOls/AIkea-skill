"""Scope: Resolve one surface pattern into shared drilling on contacting parallel panels."""

from dataclasses import replace

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from panel_blank_builder import PanelBlankBuilder
from part_construction_error import PartConstructionError
from surface_drilling_builder import SurfaceDrillingBuilder
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHolePattern


class LayeredSurfaceDrilling:
    """Emit ordinary part-local requests; never create a combined physical panel."""

    def build(self, machining_id, parts, surface_to_owner, holes):
        pattern = SurfaceHolePattern(holes)
        ids = tuple(part.part_id for part in parts)
        if not ids or len(set(ids)) != len(ids):
            raise PartConstructionError("layer drilling requires distinct physical parts")
        requests, intervals = [], {hole.hole_id: [] for hole in holes}
        surface = LocalToParentLocation().build(surface_to_owner)
        for part in parts:
            local = LocalToParentLocation().build(part.local_to_parent).inverse * surface
            origin, axes = self._frame(local)
            normal = axes[2]
            if abs(abs(normal.z)-1) > 1e-9:
                raise PartConstructionError("layer drilling requires parallel panel broad faces")
            thickness = part.local_size_mm[2]
            start = ((0 if normal.z > 0 else thickness)-origin.z)/normal.z
            end = start+thickness
            blank = PanelBlankBuilder().build(part).val()
            included = []
            for placed in pattern.place(cq.Plane.XY(), entry_clearance_mm=0):
                hole = placed.spec
                lower, upper = max(0, start), min(hole.depth_mm, end)
                if upper-lower <= 1e-9 or blank.intersect(placed.cutter.located(local)).Volume() <= 1e-6:
                    continue
                included.append(replace(hole, depth_mm=upper-lower))
                intervals[hole.hole_id].append((lower, upper))
            if not included:
                continue
            entry = origin+normal*max(0, start)
            frame = self._placement(surface_to_owner, entry, axes)
            request = SurfaceDrillingSpec(f"{machining_id}__{part.part_id}", part.part_id, frame, tuple(included))
            cutter, location = SurfaceDrillingBuilder().build(part, request)
            if cutter.located(location).cut(blank).Volume() > 1e-5:
                raise PartConstructionError("layer drilling is clipped by a physical panel edge")
            requests.append(request)
        for hole in holes:
            cursor = 0.0
            for lower, upper in sorted(intervals[hole.hole_id]):
                if abs(lower-cursor) > 1e-6:
                    raise PartConstructionError(f"{hole.hole_id}: drilling layers have a gap or overlap")
                cursor = upper
            if abs(cursor-hole.depth_mm) > 1e-6:
                raise PartConstructionError(f"{hole.hole_id}: drilling depth lacks continuous material")
        return tuple(requests)

    def _frame(self, location):
        matrix = cq.Matrix(location.wrapped.Transformation())
        origin = cq.Vector().transform(matrix)
        axes = tuple(cq.Vector(*axis).transform(matrix)-origin
                     for axis in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        return origin, axes

    def _placement(self, template, origin, axes):
        basis = template.axis_basis
        values = tuple(replace(axis, x=value.x, y=value.y, z=value.z) for axis, value in zip(
            (basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent), axes))
        return replace(template, origin_in_parent=replace(template.origin_in_parent,
            x_mm=origin.x, y_mm=origin.y, z_mm=origin.z), axis_basis=replace(basis,
            local_x_in_parent=values[0], local_y_in_parent=values[1], local_z_in_parent=values[2]))
