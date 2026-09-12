"""Scope: Describe a backing and applied frame with the shared construction tools."""

from cnc_work_area import CNC_2500_X_2000_8MM, CncWorkAreaError
from surface_pocket_spec import SurfacePocketSpec
from .construction_requirement import ConstructionRequirementSpec
from .framed_front_spec import FramedFrontSpec
from .panel_assembly import PanelAssemblyBuilder, PanelAssemblySpec
from .specification import (
    BuiltChildAssembly, ChildAssemblySpec, IDENTITY_AXIS_BASIS,
    LocalToParentPlacement, PartSpec, Point3D,
)


class FramedFrontBuilder:
    def __init__(self, spec: FramedFrontSpec, cnc_work_area=CNC_2500_X_2000_8MM):
        self.spec = spec
        self.work_area = cnc_work_area

    def _part(self, name, thickness, offset, material):
        size = (self.spec.width_mm, self.spec.height_mm, thickness)
        placement = LocalToParentPlacement(Point3D(0, 0, offset), IDENTITY_AXIS_BASIS)
        return PartSpec(name, f"front_{name}",
                        tuple(zip(("width", "height", "thickness"), size)),
                        placement, local_size_mm=size, inside_face="<Z", material_id=material)

    def recipe(self):
        if not self.work_area.fits(self.spec.width_mm, self.spec.height_mm):
            raise CncWorkAreaError("front blank exceeds the configured CNC work area")
        backing = self._part("backing", self.spec.backing_thickness_mm, 0,
                             self.spec.backing_material_id)
        frame = self._part("frame", self.spec.frame_thickness_mm,
                           self.spec.backing_thickness_mm, self.spec.frame_material_id)
        width, height = self.spec.opening_size_mm
        surface = LocalToParentPlacement(Point3D(self.spec.borders.left_mm,
            self.spec.borders.bottom_mm+height/2, 0), IDENTITY_AXIS_BASIS)
        opening = SurfacePocketSpec("frame_opening", "frame", surface, width, height,
                                    self.spec.frame_thickness_mm, self.spec.opening_corner_radius_mm)
        requirements = (
            ConstructionRequirementSpec("frame_opening", "Machine the frame opening",
                ("part:frame",), ("machining:frame_opening",), "operations"),
            ConstructionRequirementSpec("frame_attachment", "Attach the frame to its backing",
                ("part:backing", "part:frame"), basis=(
                    f"Adhesive choice: {self.spec.adhesive_product or 'unselected'}. "
                    "Material compatibility, contact preparation and strength remain unresolved.")),
            ConstructionRequirementSpec("front_mounting", "Support the complete front in its parent",
                ("part:backing", "part:frame"), basis="The parent must supply mounting and movement evidence."),
        )
        return PanelAssemblySpec(self.spec.assembly_id, self.spec.purpose, (backing, frame),
                                 machining=(opening,), requirements=requirements)

    def build(self):
        return PanelAssemblyBuilder(self.recipe()).build()

    def child(self, local_to_parent: LocalToParentPlacement):
        built = self.build()
        placement = ChildAssemblySpec(built.spec.assembly_id, built.spec.purpose, local_to_parent)
        return BuiltChildAssembly(placement, built)
