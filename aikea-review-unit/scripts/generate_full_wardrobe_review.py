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
from door_review_state import DoorReviewState
from full_wardrobe_door_plan import DoorReviewPlanError, FullWardrobeDoorPlan
from part_construction_error import PartConstructionError
from unit_mockup import UnitMockupInputError


class GenerateFullWardrobeReviewCommand:
    """Read one project and report its full-wardrobe review artifacts."""

    def run(
        self,
        path: Path,
        doors: str,
        door_assignments: tuple[str, ...] = (),
    ) -> int:
        try:
            from full_wardrobe_review_generator import FullWardrobeReviewGenerator
            from fabrication_review_proposal_writer import (
                FabricationReviewProposalWriter,
            )

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            door_plan = FullWardrobeDoorPlan.from_assignments(
                DoorReviewState(doors),
                door_assignments,
            )
            result = FullWardrobeReviewGenerator().generate(
                path.parent,
                project,
                door_plan,
            )
            fabrication_review = FabricationReviewProposalWriter().write_for_result(
                path.parent,
                result,
            )
        except (OSError, yaml.YAMLError) as error:
            return self._invalid([str(error)])
        except UnitMockupInputError as error:
            return self._invalid(list(error.problems))
        except PartConstructionError as error:
            return self._invalid([str(error)])
        except DoorReviewPlanError as error:
            return self._invalid([str(error)])
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assemblies": list(result.assembly_ids),
                    "full_wardrobe_glb": str(result.glb_path),
                    "assembly_position_check": str(result.position_report_path),
                    "doors": dict(result.door_states),
                    "fabrication_review": (
                        str(fabrication_review) if fabrication_review else None
                    ),
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
        choices=("closed", "open", "removed"),
        default="closed",
        help="Choose the default door state shown in the visual review.",
    )
    parser.add_argument(
        "--door",
        action="append",
        default=[],
        metavar="ASSEMBLY=STATE",
        help="Override one cabinet door with closed, open, or removed.",
    )
    arguments = parser.parse_args()
    return GenerateFullWardrobeReviewCommand().run(
        arguments.aikea_yaml,
        arguments.doors,
        tuple(arguments.door),
    )


if __name__ == "__main__":
    raise SystemExit(main())
