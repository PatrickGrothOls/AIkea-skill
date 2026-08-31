"""Scope: Provide the terminal command that exports one lit cabinet GLB."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [
    str(SKILL_ROOT / "aikea-build-units/scripts"),
    str(SKILL_ROOT / "aikea-build-drawers/scripts"),
    str(SKILL_ROOT / "aikea-review-unit/scripts"),
]

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from door_review_state import DoorReviewState


class GenerateCabinetLightingReviewCommand:
    """Build the generated cabinet and report its visual-review evidence."""

    def run(self, arguments: argparse.Namespace) -> int:
        from cabinet_lighting_review_generator import CabinetLightingReviewGenerator

        result = CabinetLightingReviewGenerator().generate(
            arguments.aikea_yaml.parent,
            arguments.assembly_id,
            arguments.part_id,
            base_builder_module=arguments.base_builder_module,
            hardware_directory=arguments.hardware_directory,
            door_state=DoorReviewState(arguments.door_state),
        )
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assembly_id": result.assembly_id,
                    "glb": str(result.glb_path),
                    "fit_report": str(result.fit_report_path),
                },
                indent=2,
            )
        )
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
    parser = argparse.ArgumentParser(
        description="Export one generated cabinet with its saved recessed light."
    )
    parser.add_argument("aikea_yaml", type=Path)
    parser.add_argument("--assembly-id", required=True)
    parser.add_argument("--part-id", required=True)
    parser.add_argument("--base-builder-module", default="builder")
    parser.add_argument("--hardware-directory", type=Path, required=True)
    parser.add_argument(
        "--door-state",
        choices=tuple(state.value for state in DoorReviewState),
        default=DoorReviewState.REMOVED.value,
    )
    try:
        return GenerateCabinetLightingReviewCommand().run(parser.parse_args())
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "invalid", "problems": [str(error)]}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
