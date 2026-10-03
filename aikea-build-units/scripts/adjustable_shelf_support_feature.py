"""Scope: Own four Duplo purchases and their matching side-panel bores per adjustable shelf."""
from dataclasses import dataclass, replace
import cadquery as cq
from duplo_shelf_support_profile import DuploShelfSupportProfile
from local_to_parent_location import LocalToParentLocation
from panel_machining_feature import PanelMachiningFeature
from part_construction_error import PartConstructionError
from purchased_hardware_spec import HardwarePurchaseSpec, PurchasedHardwareSpec
from surface_drilling_spec import SurfaceDrillingSpec
from surface_hole_pattern import SurfaceHole
from surface_drilling_reuse import SurfaceDrillingReuse
from system_32_side_panel_grid import System32SidePanelGridProfile


@dataclass(frozen=True)
class AdjustableShelfSupportFeature:
    shelf_ids: tuple[str, ...]
    left_side_id: str = "left_side"
    right_side_id: str = "right_side"
    front_rear_setback_mm: float = 37.0
    adjustment_row_offsets_mm: tuple[float, ...] = (0.0,)

    def apply(self, assembly):
        from assemblies.specification import BuiltPurchasedHardware, ConstructionRequirementSpec
        if not self.shelf_ids:
            return assembly
        profile = DuploShelfSupportProfile()
        purchases, requirements = [], []
        side_holes = {side:[] for side in (self.left_side_id,self.right_side_id)}
        for shelf_id in self.shelf_ids:
            shelf = assembly.spec.part(shelf_id)
            point = shelf.local_to_parent.origin_in_parent
            width, depth, _ = shelf.local_size_mm
            if shelf.local_to_parent.axis_basis.local_z_in_parent.z < .999999:
                raise PartConstructionError("Adjustable shelf supports require a horizontal shelf")
            z = point.z_mm-profile.pin_diameter_mm/2
            subjects = ["part:"+shelf_id]
            sides = ((self.left_side_id,point.x_mm-profile.shelf_side_clearance_mm,1),
                     (self.right_side_id,point.x_mm+width+profile.shelf_side_clearance_mm,-1))
            for side_id,x,direction in sides:
                side = assembly.spec.part(side_id)
                location = LocalToParentLocation().build(side.local_to_parent)
                inverse = location.inverse
                # The side owns grid columns; changing shelf clearance must not move them.
                y_positions = tuple(cq.Vector(column,0,0).transform(
                    cq.Matrix(location.wrapped.Transformation())).y for column in
                    (self.front_rear_setback_mm,side.local_size_mm[0]-self.front_rear_setback_mm))
                if any(y < point.y_mm or y > point.y_mm+depth for y in y_positions):
                    raise PartConstructionError("Shelf depth does not reach both cabinet-owned support columns")
                if side.inside_face != ">Z":
                    raise PartConstructionError("Shelf support recipe requires the side's inside broad face to be >Z")
                for index,y in enumerate(y_positions,1):
                    identity = f"{shelf_id}_{side_id}_support_{index}"
                    plane = cq.Plane(origin=(x,y,z),xDir=(0,1,0),normal=(direction,0,0))
                    purchase = PurchasedHardwareSpec(identity,profile.manufacturer,profile.article,
                        "hettich_duplo_46642_dimension_preview",self._frame(plane),
                        purchase=HardwarePurchaseSpec(identity,profile.article,"piece","item",("item",)),
                        mounting_part_id=side_id)
                    purchases.append(BuiltPurchasedHardware(purchase,profile.visual_geometry()))
                    local = cq.Vector(x,y,z).transform(cq.Matrix(inverse.wrapped.Transformation()))
                    if abs(local.z-side.local_size_mm[2]) > 1e-6:
                        raise PartConstructionError("Shelf side clearance does not align its pin with the side face")
                    side_holes[side_id].extend(SurfaceHole(f"{identity}_row_{row}",local.x,-local.y-offset,
                        profile.pin_diameter_mm,System32SidePanelGridProfile().hole_depth_mm)
                        for row,offset in enumerate(self.adjustment_row_offsets_mm))
                    subjects.append("hardware:"+identity)
            requirements.extend((ConstructionRequirementSpec(shelf_id+"_supports",
                "Install four Duplo 46642 pins in their matching blind bores",tuple(subjects),
                tuple("machining:"+side+"_adjustable_supports" for side in side_holes),"operations"),
                ConstructionRequirementSpec(shelf_id+"_support_load",
                "Confirm shelf load/deflection, stock, removal and retention for the intended use",
                ("part:"+shelf_id,),basis="Dimension-based Hettich drawing preview; no workshop load proof")))
        ids = {item.spec.hardware_id for item in purchases}
        if len(ids) != len(purchases) or ids.intersection(item.hardware_id for item in assembly.spec.purchased_hardware):
            raise PartConstructionError("Shelf support purchases must have distinct owned identities")
        drilling = tuple(self._drilling(assembly,side,holes) for side,holes in side_holes.items())
        result = PanelMachiningFeature().apply(assembly,drilling,tuple(requirements))
        return replace(result,spec=replace(result.spec,purchased_hardware=result.spec.purchased_hardware+
            tuple(item.spec for item in purchases)),purchased_hardware=result.purchased_hardware+tuple(purchases))

    def _drilling(self, assembly, side_id, holes):
        side = assembly.spec.part(side_id)
        plane = cq.Plane(origin=(0,0,side.local_size_mm[2]),xDir=(1,0,0),normal=(0,0,-1))
        operation = SurfaceDrillingSpec(side_id+"_adjustable_supports",side_id,self._frame(plane),tuple(holes))
        prior_ids = {item.machining_id for item in assembly.spec.machining}
        reuse = SurfaceDrillingReuse().matching_operations(operation,tuple(
            cut for cut in assembly.cuts if cut.joint_id in prior_ids))
        return replace(operation,reuse_machining_ids=reuse)

    def _frame(self, plane):
        from assemblies.specification import LocalToParentPlacement, Point3D, AxisBasis, AxisDirection
        return LocalToParentPlacement(Point3D(*plane.origin.toTuple()),AxisBasis(
            *(AxisDirection(*axis.toTuple()) for axis in (plane.xDir,plane.yDir,plane.zDir))))
