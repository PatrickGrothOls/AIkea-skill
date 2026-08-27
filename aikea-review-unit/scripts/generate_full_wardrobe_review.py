"""Scope: Provide the command that exports one complete wardrobe review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from part_construction_error import PartConstructionError
from unit_mockup import UnitMockupInputError


class GenerateFullWardrobeReviewCommand:
    """Read one project and report its full-wardrobe review artifacts."""

    def run(self, path: Path, doors: str) -> int:
        try:
            from door_review_pose import DoorReviewPose
            from full_wardrobe_review_generator import FullWardrobeReviewGenerator

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            result = FullWardrobeReviewGenerator().generate(
                path.parent,
                project,
                DoorReviewPose(doors),
            )
        except (OSError, yaml.YAMLError) as error:
            return self._invalid([str(error)])
        except UnitMockupInputError as error:
            return self._invalid(list(error.problems))
        except PartConstructionError as error:
            return self._invalid([str(error)])
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assemblies": list(result.assembly_ids),
                    "full_wardrobe_glb": str(result.glb_path),
                    "assembly_position_check": str(result.position_report_path),
                    "doors": result.door_pose,
                },
                indent=2,
            )
        )
        return 0

    def _invalid(self, problems: list[str]) -> int:
        print(json.dumps({"status": "invalid", "problems": problems}, indent=2))
        return 2


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
        description="Generate the complete AIkea wardrobe review."
    )
    parser.add_argument("aikea_yaml", type=Path)
    parser.add_argument(
        "--doors",
        choices=("closed", "open"),
        default="closed",
        help="Choose the door pose shown in the visual review.",
    )
    arguments = parser.parse_args()
    return GenerateFullWardrobeReviewCommand().run(
        arguments.aikea_yaml,
        arguments.doors,
    )


if __name__ == "__main__":
    raise SystemExit(main())
