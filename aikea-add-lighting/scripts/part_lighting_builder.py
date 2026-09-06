"""Scope: Cut one saved recessed-light run into its already-built host part."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

import cadquery as cq

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
        if built_part.spec.part_id != plan.part_id:
            raise ValueError("lighting plan and host part differ")
        face = self.face_frames.build(built_part.spec, plan.face)
        geometry = self.run_geometry.build(plan.run)
        lighting_in_part = face.location() * geometry.run_location
        cutter = geometry.groove_cutter.val().located(lighting_in_part)
        grooved_solid = cq.Workplane(
            obj=built_part.solid.val().cut(cutter)
        )
        return BuiltPartLighting(
            part=replace(built_part, solid=grooved_solid),
            face_frame=face,
            groove_cutter=geometry.groove_cutter,
            luminaire_body=geometry.luminaire_body,
            emitter_face=geometry.emitter_face,
            lighting_in_part=lighting_in_part,
        )


__all__ = ["BuiltPartLighting", "PartLightingBuilder"]
