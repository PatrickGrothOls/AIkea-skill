"""Scope: Cut one saved recessed-light run into its already-built host part."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import cadquery as cq

from lighting_machining_recipe import LightingMachiningRecipe
from panel_cut_applicator import PanelCutApplicator
from part_cut import PartCut
from surface_groove_builder import SurfaceGrooveBuilder
from lighting_run_geometry import LightingRunGeometryBuilder
from part_face_frame import PartFaceFrame
from part_face_frame import PartFaceFrameBuilder
from part_lighting_plan import PartLightingPlan


@dataclass(frozen=True, slots=True)
class BuiltPartLighting:
    """Retain the machined part and every aligned review solid."""

    part: Any
    face_frame: PartFaceFrame
    groove_cutter: cq.Workplane
    luminaire_body: cq.Workplane
    emitter_face: cq.Workplane
    lighting_in_part: cq.Location


class PartLightingBuilder:
    """Apply one plan without rebuilding or discarding earlier part machining."""

    def __init__(self) -> None:
        self.face_frames = PartFaceFrameBuilder()
        self.run_geometry = LightingRunGeometryBuilder()

    def build(self, built_part: Any, plan: PartLightingPlan) -> BuiltPartLighting:
        prepared = self.prepare(built_part, plan)
        request = LightingMachiningRecipe().build(built_part.spec, plan)
        cutter, location = SurfaceGrooveBuilder().build(built_part.spec, request)
        cut = PartCut(request.machining_id, plan.part_id, 1, cutter, location)
        solid = PanelCutApplicator().apply(built_part.spec, built_part.solid, (cut,), {request.machining_id: request})
        return replace(prepared, part=replace(built_part, solid=solid))

    def prepare(self, built_part, plan):
        """Derive aligned review solids without altering the host part."""
        if built_part.spec.part_id != plan.part_id:
            raise ValueError("lighting plan and host part differ")
        face = self.face_frames.build(built_part.spec, plan.face)
        geometry = self.run_geometry.build(plan.run)
        lighting_in_part = face.location() * geometry.run_location
        return BuiltPartLighting(built_part, face, geometry.groove_cutter,
            geometry.luminaire_body, geometry.emitter_face, lighting_in_part)


__all__ = ["BuiltPartLighting", "PartLightingBuilder"]
