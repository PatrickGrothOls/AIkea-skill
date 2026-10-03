"""Scope: Build machining, purchased-body, and emitter geometry from one light run."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

from lighting_run import LightingRun


@dataclass(frozen=True, slots=True)
class LightingRunGeometry:
    """Keep every solid and its shared face-local placement together."""

    groove_cutter: cq.Workplane
    luminaire_body: cq.Workplane
    emitter_face: cq.Workplane
    run_location: cq.Location


class LightingRunGeometryBuilder:
    """Derive one coordinated geometry set from a saved run."""

    EMITTER_THICKNESS_MM = 0.2

    def build(self, run: LightingRun) -> LightingRunGeometry:
        profile = run.profile
        cutter = self._centered_box(
            run.length_mm,
            profile.groove_width_mm,
            profile.groove_depth_mm,
        ).translate((0.0, 0.0, -profile.groove_depth_mm))
        body = self._centered_box(
            run.length_mm,
            profile.groove_width_mm,
            profile.groove_depth_mm,
        ).translate((0.0, 0.0, -profile.groove_depth_mm))
        emitter = self._centered_box(
            run.length_mm,
            profile.groove_width_mm * 0.8,
            self.EMITTER_THICKNESS_MM,
        )
        location = cq.Location(
            cq.Vector(run.start_mm[0], run.start_mm[1], 0.0),
            cq.Vector(0.0, 0.0, 1.0),
            run.angle_degrees,
        )
        return LightingRunGeometry(cutter, body, emitter, location)

    def _centered_box(
        self,
        length_mm: float,
        width_mm: float,
        depth_mm: float,
    ) -> cq.Workplane:
        return cq.Workplane("XY").box(
            length_mm,
            width_mm,
            depth_mm,
            centered=(False, True, False),
        )


__all__ = ["LightingRunGeometry", "LightingRunGeometryBuilder"]
