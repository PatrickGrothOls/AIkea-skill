"""Scope: Provide the command for a full wardrobe drawer-collection review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
DRAWER_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-drawers" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))
sys.path.insert(0, str(DRAWER_SCRIPTS))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from door_review_state import DoorReviewState
from full_wardrobe_door_plan import FullWardrobeDoorPlan
from unit_mockup import UnitMockupInputError


class GenerateDrawerCollectionWardrobeReviewCommand:
    """Parse independent drawer poses and export their existing wardrobe."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate an AIkea wardrobe with independently posed drawers."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        parser.add_argument(
            "--drawer-extension",
            action="append",
            default=[],
            metavar="CABINET:DRAWER:MM",
        )
        parser.add_argument(
            "--doors",
            choices=[state.value for state in DoorReviewState],
            default=DoorReviewState.CLOSED.value,
        )
        parser.add_argument(
            "--door",
            action="append",
            default=[],
            metavar="CABINET=STATE",
        )
        parser.add_argument(
            "--output-filename",
            default="full_wardrobe_drawer_collection_review.glb",
        )
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        from drawer_collection_wardrobe_review_generator import (
            DrawerCollectionWardrobeReviewGenerator,
        )

        project = yaml.safe_load(arguments.aikea_yaml.read_text(encoding="utf-8"))
        try:
            result = DrawerCollectionWardrobeReviewGenerator().generate(
                arguments.aikea_yaml.parent,
                project,
                arguments.hardware_directory.resolve(),
                self._extensions(arguments.drawer_extension),
                FullWardrobeDoorPlan.from_assignments(
                    DoorReviewState(arguments.doors),
                    tuple(arguments.door),
                ),
                arguments.output_filename,
            )
        except (KeyError, OSError, UnitMockupInputError, ValueError) as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        print(
            json.dumps(
                {
                    "status": "generated-for-visual-approval",
                    "glb": str(result.glb_path),
                    "cabinet_position_reports": [
                        str(path) for path in result.cabinet_report_paths
                    ],
                    "full_position_report": str(result.full_position_report_path),
                    "automated_evals_run": False,
                },
                indent=2,
            )
        )
        return 0

    def _extensions(self, values: list[str]) -> dict[str, dict[str, float]]:
        resolved: dict[str, dict[str, float]] = {}
        for value in values:
            cabinet_id, separator, remainder = value.partition(":")
            drawer_id, second_separator, amount = remainder.partition(":")
            if not separator or not second_separator:
                raise ValueError(
                    "drawer extension must use CABINET:DRAWER:MM"
                )
            resolved.setdefault(cabinet_id, {})[drawer_id] = float(amount)
        return resolved


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
    arguments = GenerateDrawerCollectionWardrobeReviewCommand.parser().parse_args()
    return GenerateDrawerCollectionWardrobeReviewCommand().run(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
