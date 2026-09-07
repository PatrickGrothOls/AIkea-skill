"""Scope: Build and place a backing panel and continuous applied frame as one leaf."""

import cadquery as cq
from cnc_work_area import CNC_2500_X_2000_8MM, CncWorkAreaError
from .framed_front_spec import AppliedFrameGlueJoint, FramedFrontSpec
from .panel_assembly import PanelAssemblySpec, PanelBlankBuilder
from .specification import (
    BuiltAssembly, BuiltChildAssembly, BuiltPart, ChildAssemblySpec,
    IDENTITY_AXIS_BASIS, LocalToParentPlacement, PartSpec, Point3D,
)


class FramedFrontBuilder:
    def __init__(self, spec: FramedFrontSpec, cnc_work_area=CNC_2500_X_2000_8MM):
        self.spec = spec
        self.work_area = cnc_work_area
        self.blanks = PanelBlankBuilder()

    def _part(self, name, thickness, offset):
        size = (self.spec.width_mm, self.spec.height_mm, thickness)
        placement = LocalToParentPlacement(Point3D(0, 0, offset), IDENTITY_AXIS_BASIS)
        return PartSpec(name, f"front_{name}",
                        tuple(zip(("width", "height", "thickness"), size)),
                        placement, local_size_mm=size, inside_face="<Z")

    def _opening(self):
        width, height = self.spec.opening_size_mm
        opening = cq.Workplane("XY").box(width, height, self.spec.frame_thickness_mm,
                                          centered=(False, False, False))
        radius = self.spec.opening_corner_radius_mm
        if radius:
            opening = opening.edges("|Z").fillet(radius)
        return opening.translate((self.spec.borders.left_mm,
                                  self.spec.borders.bottom_mm, 0))

    def build(self):
        if not self.work_area.fits(self.spec.width_mm, self.spec.height_mm):
            raise CncWorkAreaError("front blank exceeds the configured CNC work area")
        backing = self._part("backing", self.spec.backing_thickness_mm, 0)
        frame = self._part("frame", self.spec.frame_thickness_mm,
                           self.spec.backing_thickness_mm)
        parts = (BuiltPart(backing, self.blanks.build(backing)),
                 BuiltPart(frame, self.blanks.build(frame).cut(self._opening())))
        joint = AppliedFrameGlueJoint(self.spec.adhesive_product)
        assembly = PanelAssemblySpec(self.spec.assembly_id, self.spec.purpose,
                                      (backing, frame), (joint,))
        # A glued contact removes no material, so this joint supplies no fictitious cuts.
        return BuiltAssembly(assembly, parts, (joint,))

    def child(self, local_to_parent: LocalToParentPlacement):
        built = self.build()
        placement = ChildAssemblySpec(built.spec.assembly_id, built.spec.purpose,
                                      local_to_parent)
        return BuiltChildAssembly(placement, built)
