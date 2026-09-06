"""Scope: Provide the visual-approval command for one recessed-light panel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPTS = SKILL_ROOT / "aikea-build-units" / "scripts"
REVIEW_SCRIPTS = SKILL_ROOT / "aikea-review-unit" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))
sys.path.insert(0, str(REVIEW_SCRIPTS))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from lighting_run import LightingRun
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class GenerateLightingPanelReviewCommand:
    """Create one saved run, its machining, and its review model."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Generate a recessed-light panel review.")
        parser.add_argument("--output-directory", required=True, type=Path)
        parser.add_argument("--panel-width-mm", type=float, default=300.0)
        parser.add_argument("--panel-height-mm", type=float, default=600.0)
        parser.add_argument("--panel-thickness-mm", type=float, default=18.0)
        parser.add_argument("--run-start-mm", nargs=2, type=float)
        parser.add_argument("--run-end-mm", nargs=2, type=float)
        parser.add_argument("--color-temperature-k", type=int, default=3200)
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        from lighting_panel_review_generator import LightingPanelReviewGenerator

        start = tuple(arguments.run_start_mm or (50.0, 0.0))
        end = tuple(arguments.run_end_mm or (50.0, arguments.panel_height_mm))
        try:
            run = LightingRun(
                "side_lighting_01",
                start,
                end,
                arguments.color_temperature_k,
                DOMUS_APEX_84_HI,
            )
            result = LightingPanelReviewGenerator().generate(
                arguments.output_directory.resolve(),
                arguments.panel_width_mm,
                arguments.panel_height_mm,
                arguments.panel_thickness_mm,
                run,
            )
        except (OSError, ValueError) as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        print(json.dumps({
            "status": "generated-for-visual-approval",
            "glb": str(result.glb_path),
            "lighting_run": str(result.run_path),
            "fit_report": str(result.fit_report_path),
            "automated_evals_run": False,
        }, indent=2))
        return 0


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
    arguments = GenerateLightingPanelReviewCommand.parser().parse_args()
    return GenerateLightingPanelReviewCommand().run(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
