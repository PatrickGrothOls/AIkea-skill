"""Scope: Convert one saved light run into an explicit common surface-groove request."""

from dataclasses import replace

import cadquery as cq

from lighting_run_geometry import LightingRunGeometryBuilder
from part_face_frame import PartFaceFrameBuilder
from rigid_frame import RigidFrame
from surface_groove_spec import SurfaceGrooveSpec


class LightingMachiningRecipe:
    def build(self, part, plan):
        if part.part_id != plan.part_id:
            raise ValueError("lighting plan and host part differ")
        face = PartFaceFrameBuilder().build(part, plan.face)
        run = LightingRunGeometryBuilder().build(plan.run)
        inward = face.location()*run.run_location*cq.Location(cq.Vector(), cq.Vector(1, 0, 0), 180)
        frame = RigidFrame.from_location(inward)
        original = part.local_to_parent
        basis = original.axis_basis
        axes = tuple(replace(axis, x=direction[0], y=direction[1], z=direction[2]) for axis, direction in zip(
            (basis.local_x_in_parent, basis.local_y_in_parent, basis.local_z_in_parent),
            (frame.local_x_in_parent, frame.local_y_in_parent, frame.local_z_in_parent)))
        placement = replace(original, origin_in_parent=replace(original.origin_in_parent,
            x_mm=frame.origin_mm[0], y_mm=frame.origin_mm[1], z_mm=frame.origin_mm[2]),
            axis_basis=replace(basis, local_x_in_parent=axes[0], local_y_in_parent=axes[1], local_z_in_parent=axes[2]))
        return SurfaceGrooveSpec(plan.run.run_id+"_groove", part.part_id, placement,
            plan.run.length_mm, plan.run.profile.groove_width_mm, plan.run.profile.groove_depth_mm)
