"""Scope: Provide the single-cabinet KA 4532 spacer proof command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[2]
for skill_name in ("aikea-build-units", "aikea-review-unit"):
    sys.path.insert(0, str(SKILL_ROOT / skill_name / "scripts"))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError


class GenerateHettichKa4532SpacerCabinetDrawerCommand:
    """Save one exact installed set and report its fabrication blocker."""

    def parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate one AIkea drawer with KA 4532 and spacer 13952."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--drawer", default="drawer_01")
        parser.add_argument("--bottom-height-mm", required=True, type=float)
        parser.add_argument("--box-height-mm", default=160.0, type=float)
        parser.add_argument("--box-depth-mm", default=500.0, type=float)
        parser.add_argument("--cabinet-front-mm", default=0.0, type=float)
        parser.add_argument("--drawer-front-mm", required=True, type=float)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        from cabinet_drawer_plan import DrawerLayout
        from hettich_ka_4532_spacer_cabinet_drawer_generator import (
            HettichKa4532SpacerCabinetDrawerGenerator,
        )

        try:
            result = HettichKa4532SpacerCabinetDrawerGenerator().generate(
                arguments.aikea_yaml.resolve().parent,
                arguments.assembly,
                DrawerLayout(
                    arguments.drawer,
                    arguments.bottom_height_mm,
                    box_height_mm=arguments.box_height_mm,
                    box_depth_mm=arguments.box_depth_mm,
                ),
                hardware_directory=arguments.hardware_directory.resolve(),
                cabinet_front_mm=arguments.cabinet_front_mm,
                drawer_front_mm=arguments.drawer_front_mm,
            )
        except ValueError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        plan = result.plan
        print(
            json.dumps(
                {
                    "status": "generated-for-single-cabinet-proof",
                    "assembly": plan.parent_assembly_id,
                    "drawer": plan.drawer.assembly_id,
                    "runner_item_number": plan.hardware.runner_item_number,
                    "spacer_item_number": plan.hardware.spacer_item_number,
                    "spacer_instances": 2,
                    "combined_load_capacity_kg": plan.hardware.combined_load_capacity_kg,
                    "fabrication_ready": False,
                    "machining_authority": plan.machining_authority,
                    "written": [str(path) for path in result.written_paths],
                },
                indent=2,
            )
        )
        return 0


# This direct adapter keeps Python's CLI entry point outside the command object.
def main() -> int:
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
    command = GenerateHettichKa4532SpacerCabinetDrawerCommand()
    return command.run(command.parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
