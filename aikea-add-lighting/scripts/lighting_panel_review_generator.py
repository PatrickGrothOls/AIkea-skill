"""Scope: Export one standalone recessed-light panel for visual approval."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import cadquery as cq
import yaml

from cadquery_glb_exporter import CadQueryGlbExporter
from lighting_groove_geometry import LightingGrooveGeometry
from lighting_panel_fit_checker import LightingPanelFitChecker
from lighting_run import LightingRun
from unit_mockup import MockupPart


@dataclass(frozen=True, slots=True)
class LightingPanelReviewResult:
    """Expose the review model and its two written evidence files."""

    glb_path: Path
    run_path: Path
    fit_report_path: Path


class LightingPanelReviewGenerator:
    """Create a grooved panel and matching complete-luminaire preview."""

    def __init__(self) -> None:
        self.geometry = LightingGrooveGeometry()
        self.fit_checker = LightingPanelFitChecker()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        output_directory: Path,
        panel_width_mm: float,
        panel_height_mm: float,
        panel_thickness_mm: float,
        run: LightingRun,
    ) -> LightingPanelReviewResult:
        built = self.geometry.build(
            panel_width_mm,
            panel_height_mm,
            panel_thickness_mm,
            run,
        )
        fit = self.fit_checker.check(
            panel_width_mm,
            panel_height_mm,
            panel_thickness_mm,
            run,
            built,
        )
        if fit.status != "pass":
            raise ValueError("the recessed light does not fit its host panel")
        output_directory.mkdir(parents=True, exist_ok=True)
        glb_path = output_directory / "recessed_light_panel.glb"
        run_path = output_directory / "lighting_run.yaml"
        fit_report_path = output_directory / "lighting_fit_report.json"
        parts = (
            MockupPart(
                "lighting_test_panel",
                built.panel,
                cq.Location(),
                (0.75, 0.58, 0.36, 1.0),
            ),
            MockupPart(
                f"purchased_light__{run.profile.profile_id}__body",
                built.luminaire_body,
                built.run_location,
                (0.23, 0.24, 0.22, 1.0),
            ),
            MockupPart(
                f"light_source__{run.profile.profile_id}__{run.color_temperature_k}k",
                built.emitter_face,
                built.run_location,
                self._light_color(run.color_temperature_k),
            ),
        )
        self.exporter.export("recessed_light_panel", parts, glb_path)
        run_path.write_text(yaml.safe_dump(run.as_record(), sort_keys=False))
        fit_report_path.write_text(json.dumps(fit.as_record(), indent=2) + "\n")
        return LightingPanelReviewResult(glb_path, run_path, fit_report_path)

    def _light_color(self, temperature_k: int) -> tuple[float, float, float, float]:
        return {
            2900: (1.0, 0.68, 0.38, 1.0),
            3200: (1.0, 0.76, 0.50, 1.0),
            4300: (1.0, 0.90, 0.74, 1.0),
        }[temperature_k]


__all__ = ["LightingPanelReviewGenerator", "LightingPanelReviewResult"]
