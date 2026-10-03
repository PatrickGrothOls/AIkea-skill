"""Scope: Provide the command for the visual KA 5332 approval gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
DRAWER_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-drawers" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))
sys.path.insert(0, str(DRAWER_SCRIPTS))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from hardware_asset_resolver import HardwareAssetError
from hardware_step_importer import HardwareStepImportError
from unit_mockup import UnitMockupInputError


class GenerateHettichKa5332PrototypeCommand:
    """Build three review states without advancing to automated checks."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate the Hettich KA 5332 visual prototype."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        parser.add_argument("--output-directory", required=True, type=Path)
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        try:
            from hettich_ka_5332_prototype_generator import (
                HettichKa5332PrototypeGenerator,
            )

            result = HettichKa5332PrototypeGenerator().generate(
                arguments.aikea_yaml.parent,
                arguments.assembly,
                arguments.hardware_directory.resolve(),
                arguments.output_directory.resolve(),
            )
        except (
            HardwareAssetError,
            HardwareStepImportError,
            OSError,
            UnitMockupInputError,
            ValueError,
        ) as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        print(
            json.dumps(
                {
                    "status": "generated-for-visual-approval",
                    "closed_glb": str(result.closed_glb),
                    "open_glb": str(result.open_glb),
                    "removed_glb": str(result.removed_glb),
                    "closed_connection_glb": str(result.closed_connection_glb),
                    "open_connection_glb": str(result.open_connection_glb),
                    "removed_connection_glb": str(
                        result.removed_connection_glb
                    ),
                    "drawer_outside_width_mm": result.drawer_outside_width_mm,
                    "manufacturer_width_recommendation_met": (
                        result.recommended_width_met
                    ),
                    "minimum_cabinet_depth_met": result.minimum_depth_met,
                    "automated_checks_run": False,
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
    arguments = GenerateHettichKa5332PrototypeCommand.parser().parse_args()
    return GenerateHettichKa5332PrototypeCommand().run(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
