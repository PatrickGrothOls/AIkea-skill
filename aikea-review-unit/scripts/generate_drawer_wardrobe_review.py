"""Scope: Provide the command that exports one drawer-in-wardrobe review."""

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
from drawer_review_state import DrawerReviewState
from hardware_asset_resolver import HardwareAssetError
from hardware_step_importer import HardwareStepImportError
from unit_mockup import UnitMockupInputError


class GenerateDrawerWardrobeReviewCommand:
    """Read one project and report its drawer review artifacts."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate one drawer wardrobe review."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        parser.add_argument(
            "--drawer-state",
            choices=tuple(state.value for state in DrawerReviewState),
            default=DrawerReviewState.OPEN.value,
        )
        return parser

    def run(
        self,
        path: Path,
        assembly_id: str,
        hardware_directory: Path,
        drawer_state: str,
    ) -> int:
        try:
            from drawer_wardrobe_review_generator import DrawerWardrobeReviewGenerator

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            result = DrawerWardrobeReviewGenerator().generate(
                path.parent,
                project,
                assembly_id,
                hardware_directory,
                DrawerReviewState(drawer_state),
            )
        except (OSError, yaml.YAMLError) as error:
            return self._invalid([str(error)])
        except UnitMockupInputError as error:
            return self._invalid(list(error.problems))
        except (HardwareAssetError, HardwareStepImportError) as error:
            return self._invalid([str(error)])
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assembly": result.assembly_id,
                    "drawer": result.drawer_id,
                    "drawer_state": result.drawer_state,
                    "runner_product_code": result.runner_product_code,
                    "runner_review": result.runner_review_representation,
                    "closeup_glb": str(result.closeup_glb_path),
                    "full_wardrobe_glb": str(result.full_wardrobe_glb_path),
                    "drawer_position_check": str(
                        result.drawer_position_report_path
                    ),
                    "hardware_position_check": str(
                        result.hardware_position_report_path
                    ),
                    "runner_movement_check": str(
                        result.runner_movement_report_path
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
    arguments = GenerateDrawerWardrobeReviewCommand.parser().parse_args()
    return GenerateDrawerWardrobeReviewCommand().run(
        arguments.aikea_yaml,
        arguments.assembly,
        arguments.hardware_directory,
        arguments.drawer_state,
    )


if __name__ == "__main__":
    raise SystemExit(main())
