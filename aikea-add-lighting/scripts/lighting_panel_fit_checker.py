"""Scope: Check one light run against its host sheet and machined groove."""

from __future__ import annotations

from lighting_groove_geometry import LightingPanelGeometry
from lighting_panel_fit_report import LightingPanelFitReport
from lighting_run import LightingRun
from lighting_run_boundary_checker import LightingRunBoundaryChecker


class LightingPanelFitChecker:
    """Verify placement, retained material, and purchased-body clearance."""

    VOLUME_TOLERANCE_MM3 = 0.001

    def __init__(self) -> None:
        self.boundary = LightingRunBoundaryChecker()

    def check(
        self,
        panel_width_mm: float,
        panel_height_mm: float,
        panel_thickness_mm: float,
        run: LightingRun,
        geometry: LightingPanelGeometry,
    ) -> LightingPanelFitReport:
        inside = self.boundary.is_inside(
            panel_width_mm,
            panel_height_mm,
            run,
        )
        remaining = panel_thickness_mm - run.profile.groove_depth_mm
        groove_within_thickness = remaining >= 0.0
        placed_body = geometry.luminaire_body.val().located(geometry.run_location)
        overlap = geometry.panel.val().intersect(placed_body).Volume()
        body_fits = overlap <= self.VOLUME_TOLERANCE_MM3
        passed = inside and groove_within_thickness and body_fits
        return LightingPanelFitReport(
            status="pass" if passed else "fail",
            run_inside_panel=inside,
            groove_within_thickness=groove_within_thickness,
            remaining_panel_thickness_mm=remaining,
            body_panel_overlap_mm3=overlap,
            purchased_body_fits_groove=body_fits,
        )

__all__ = ["LightingPanelFitChecker"]
