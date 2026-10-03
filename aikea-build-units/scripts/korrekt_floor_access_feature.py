"""Scope: Continue selected Korrekt adjustment axes through a separate cabinet floor owner."""
from dataclasses import dataclass
import cadquery as cq
from local_to_parent_location import LocalToParentLocation
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from korrekt_mounting_profile import KorrektMountingProfile


@dataclass(frozen=True)
class KorrektFloorAccessFeature:
    floor_part_id: str
    axes_xy_mm: tuple[tuple[float,float], ...]

    def apply(self, assembly):
        from assemblies.specification import LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
        from assemblies.specification import ConstructionRequirementSpec
        floor = assembly.spec.part(self.floor_part_id)
        if floor.local_to_parent.axis_basis.local_z_in_parent.z < .999999:
            raise PartConstructionError("Korrekt floor access requires a horizontal cabinet floor")
        inverse = LocalToParentLocation().build(floor.local_to_parent).inverse
        thickness = floor.local_size_mm[2]
        z = floor.local_to_parent.origin_in_parent.z_mm+thickness
        points = tuple(cq.Vector(x,y,z).transform(cq.Matrix(inverse.wrapped.Transformation()))
                       for x,y in self.axes_xy_mm)
        frame = LocalToParentPlacement(Point3D(0,0,thickness),AxisBasis(
            AxisDirection(1,0,0),AxisDirection(0,-1,0),AxisDirection(0,0,-1)))
        identity = self.floor_part_id+"_korrekt_adjustment_access"
        request = SurfaceDrillingSpec(identity,self.floor_part_id,frame,tuple(
            SurfaceHole(f"axis_{i}",p.x,-p.y,KorrektMountingProfile().adjustment_diameter_mm,thickness)
            for i,p in enumerate(points,1)))
        requirement = ConstructionRequirementSpec(identity,"Keep the foot adjustment route accessible through the cabinet floor",
            ("part:"+self.floor_part_id,),("machining:"+identity,),"operations")
        return PanelMachiningFeature().apply(assembly,(request,),(requirement,))
