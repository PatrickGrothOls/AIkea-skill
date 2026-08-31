"""Scope: Build one recessed-light groove and its matching purchased-light envelope."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

from blank_sheet_builder import BlankSheetBuilder
from lighting_run import LightingRun
from lighting_run_geometry import LightingRunGeometryBuilder


@dataclass(frozen=True, slots=True)
class LightingPanelGeometry:
    """Hold the solids derived from one part-local light run."""

    panel: cq.Workplane
    groove_cutter: cq.Workplane
    luminaire_body: cq.Workplane
    emitter_face: cq.Workplane
    run_location: cq.Location


class LightingGrooveGeometry:
    """Derive panel machining and review geometry from the same run."""

    def __init__(self) -> None:
        self.run_geometry = LightingRunGeometryBuilder()

    def build(
        self,
        panel_width_mm: float,
        panel_height_mm: float,
        panel_thickness_mm: float,
        run: LightingRun,
    ) -> LightingPanelGeometry:
        blank = BlankSheetBuilder.rectangle(
            panel_width_mm,
            panel_height_mm,
            panel_thickness_mm,
        ).build().translate((0.0, 0.0, -panel_thickness_mm))
        geometry = self.run_geometry.build(run)
        return LightingPanelGeometry(
            panel=blank.cut(
                geometry.groove_cutter.val().located(geometry.run_location)
            ),
            groove_cutter=geometry.groove_cutter,
            luminaire_body=geometry.luminaire_body,
            emitter_face=geometry.emitter_face,
            run_location=geometry.run_location,
        )


__all__ = ["LightingGrooveGeometry", "LightingPanelGeometry"]
