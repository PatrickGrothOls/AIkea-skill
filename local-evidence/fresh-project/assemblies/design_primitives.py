"""Scope: Author explicit sheet frames, shared operations and purchase identities."""
from assemblies.specification import (PartSpec, BoundaryPoint, LocalToParentPlacement,
    Point3D, AxisBasis, AxisDirection, PurchasedHardwareSpec, HardwarePurchaseSpec,
    BuiltPurchasedHardware, ConstructionRequirementSpec)
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from surface_groove_spec import SurfaceGrooveSpec
import cadquery as cq


class DesignPrimitives:
    def frame(self, origin=(0,0,0), x=(1,0,0), y=(0,1,0), z=(0,0,1)):
        return LocalToParentPlacement(Point3D(*origin),AxisBasis(*(AxisDirection(*a) for a in (x,y,z))))

    def panel(self, name, size, origin=(0,0,0), axes=None, face='>Z', role='panel', outline=(), material='painted_mdf_16'):
        placement=self.frame(origin,*(axes or ((1,0,0),(0,1,0),(0,0,1))))
        return PartSpec(name,role,(),placement,tuple(BoundaryPoint(*p) for p in outline),size,face,material)

    def drill(self, name, part, coordinates, diameter, depth, face=None):
        top=(face or part.inside_face)=='>Z'
        w,h,t=part.local_size_mm
        origin,axes=((0,h,t),((1,0,0),(0,-1,0),(0,0,-1))) if top else ((0,0,0),((1,0,0),(0,1,0),(0,0,1)))
        holes=tuple(SurfaceHole(f'axis_{i:02d}',x,h-y if top else y,diameter,depth) for i,(x,y) in enumerate(coordinates))
        return SurfaceDrillingSpec(name,part.part_id,self.frame(origin,*axes),holes)

    def groove(self,name,part,start,length,width,depth,direction=(1,0),face=None):
        top=(face or part.inside_face)=='>Z'
        dx,dy=direction;z=-1 if top else 1
        frame=self.frame((*start,part.local_size_mm[2] if top else 0),(dx,dy,0),(-z*dy,z*dx,0),(0,0,z))
        return SurfaceGrooveSpec(name,part.part_id,frame,length,width,depth)

    def hardware(self,name,manufacturer,article,solid,placement=None,parent=None,purchase=None):
        spec=PurchasedHardwareSpec(name,manufacturer,article,'project-'+name,placement or self.frame(),
            purchase=purchase or HardwarePurchaseSpec(name,article,'piece','item',('item',)),mounting_part_id=parent)
        return BuiltPurchasedHardware(spec,solid if isinstance(solid,cq.Workplane) else cq.Workplane(obj=solid))

    def unresolved(self,name,subjects,description):
        return ConstructionRequirementSpec(name,description,tuple(subjects),basis='Geometry supplied; physical qualification remains explicit.')


P=DesignPrimitives()
