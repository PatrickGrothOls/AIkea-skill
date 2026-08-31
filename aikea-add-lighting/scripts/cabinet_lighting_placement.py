"""Scope: Compose a host part's light run into its cabinet coordinate frame."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cadquery as cq

from assembly_part_locator import AssemblyPartLocator
from lighting_run_geometry import LightingRunGeometryBuilder
from part_face_frame import PartFaceFrameBuilder
from part_lighting_plan import PartLightingPlan
from rigid_frame import RigidFrame


@dataclass(frozen=True, slots=True)
class CabinetLightingPlacement:
    """Expose each frame in the path from host part to cabinet."""

    part_in_cabinet: RigidFrame
    face_in_part: RigidFrame
    run_in_face: RigidFrame
    luminaire_in_cabinet: RigidFrame
    luminaire_location: cq.Location

    def as_record(self) -> dict[str, object]:
        return {
            "part_in_cabinet": self.part_in_cabinet.as_record(),
            "face_in_part": self.face_in_part.as_record(),
            "run_in_face": self.run_in_face.as_record(),
            "luminaire_in_cabinet": self.luminaire_in_cabinet.as_record(),
        }


class CabinetLightingPlacementBuilder:
    """Compose existing project frames without inventing cabinet coordinates."""

    def __init__(self) -> None:
        self.part_locator = AssemblyPartLocator()
        self.face_frames = PartFaceFrameBuilder()
        self.run_geometry = LightingRunGeometryBuilder()

    def build(
        self,
        assembly: Any,
        part: Any,
        plan: PartLightingPlan,
    ) -> CabinetLightingPlacement:
        part_location = self.part_locator.locate(
            part,
            assembly,
            float(assembly.base_height_mm),
        )
        face_location = self.face_frames.build(part, plan.face).location()
        run_location = self.run_geometry.build(plan.run).run_location
        luminaire_location = part_location * face_location * run_location
        return CabinetLightingPlacement(
            RigidFrame.from_location(part_location),
            RigidFrame.from_location(face_location),
            RigidFrame.from_location(run_location),
            RigidFrame.from_location(luminaire_location),
            luminaire_location,
        )


__all__ = ["CabinetLightingPlacement", "CabinetLightingPlacementBuilder"]
