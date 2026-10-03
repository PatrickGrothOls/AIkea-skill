"""Scope: Resolve opposite inside faces and transform rail-support fixing datums."""
from dataclasses import dataclass
from math import isfinite
import cadquery as cq
from local_to_parent_location import LocalToParentLocation
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole


@dataclass(frozen=True)
class HangingRailLayout:
    rail_id: str
    left_side_id: str
    right_side_id: str
    depth_position_mm: float
    lower_screw_height_mm: float
    pilot_diameter_mm: float = 3.0
    pilot_depth_mm: float = 13.0

    def resolve(self, assembly, profile):
        dimensions = (self.depth_position_mm, self.lower_screw_height_mm,
                      self.pilot_diameter_mm, self.pilot_depth_mm)
        if not all(isfinite(v) for v in dimensions) or not 0 < self.pilot_diameter_mm < 4:
            raise ValueError('Hanging rail needs finite datums and a pilot smaller than the 4 mm screw')
        stations = []
        for side_id, direction in ((self.left_side_id, 1), (self.right_side_id, -1)):
            side = assembly.spec.part(side_id)
            axis = side.local_to_parent.axis_basis.local_z_in_parent
            if (side.inside_face != '>Z' or abs(axis.x-direction) > 1e-6
                    or abs(side.local_to_parent.axis_basis.local_y_in_parent.z-1) > 1e-6):
                raise ValueError('Hanging rail requires opposite inward-facing vertical sides')
            if not 0 < self.pilot_depth_mm < side.local_size_mm[2]:
                raise ValueError('Hanging rail pilots must remain blind within the selected stock')
            placement = LocalToParentLocation().build(side.local_to_parent)
            face = cq.Vector(0, 0, side.local_size_mm[2]).transform(cq.Matrix(placement.wrapped.Transformation()))
            point = cq.Vector(face.x, self.depth_position_mm, self.lower_screw_height_mm)
            local = point.transform(cq.Matrix(placement.inverse.wrapped.Transformation()))
            width, height, thickness = side.local_size_mm
            if not (9.3 <= local.x <= width-9.3 and 5.4 <= local.y <= height-37.4):
                raise ValueError('Complete hanging-rail support must remain inside its side panel')
            holes = tuple(SurfaceHole(f'{self.rail_id}_{side_id}_{n}', local.x,
                -local.y-offset, self.pilot_diameter_mm, self.pilot_depth_mm)
                for n, offset in enumerate(profile.screw_offsets_mm, 1))
            surface = cq.Plane(origin=(0, 0, thickness), xDir=(1, 0, 0), normal=(0, 0, -1))
            drilling = SurfaceDrillingSpec(f'{self.rail_id}_{side_id}_fixings', side_id,
                                          self.frame(surface), holes)
            support = cq.Plane(origin=point, xDir=(direction, 0, 0), normal=(0, 0, 1))
            stations.append((side_id, point, self.frame(support), drilling))
        length = stations[1][1].x-stations[0][1].x-2*profile.end_allowance_mm
        if not 0 < length <= profile.stock_length_mm:
            raise ValueError('Hanging rail clear opening must fit the selected stock length')
        return tuple(stations), length

    @staticmethod
    def frame(plane):
        from assemblies.specification import LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
        return LocalToParentPlacement(Point3D(*plane.origin.toTuple()), AxisBasis(
            *(AxisDirection(*axis.toTuple()) for axis in (plane.xDir, plane.yDir, plane.zDir))))
