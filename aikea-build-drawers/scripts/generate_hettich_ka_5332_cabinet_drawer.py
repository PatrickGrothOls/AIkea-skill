"""Scope: Provide the command that saves one KA 5332 cabinet drawer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
REVIEW_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-review-unit" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))
sys.path.insert(0, str(REVIEW_SCRIPTS))

from cabinet_drawer_plan import DrawerLayout
from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from hettich_ka_5332_cabinet_drawer_generator import (
    HettichKa5332CabinetDrawerGenerator,
)


class GenerateHettichKa5332CabinetDrawerCommand:
    """Create the drawer child, runner plan, and composed cabinet builder."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate one AIkea cabinet drawer with KA 5332 runners."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--drawer", default="drawer_01")
        parser.add_argument("--bottom-height-mm", required=True, type=float)
        parser.add_argument("--box-height-mm", default=160.0, type=float)
        parser.add_argument("--box-depth-mm", type=float)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        return parser

    def run(
        self,
        aikea_yaml: Path,
        assembly_id: str,
        drawer_id: str,
        bottom_height_mm: float,
        box_height_mm: float,
        box_depth_mm: float | None,
        hardware_directory: Path,
    ) -> int:
        result = HettichKa5332CabinetDrawerGenerator().generate(
            aikea_yaml.parent,
            assembly_id,
            DrawerLayout(
                drawer_id,
                bottom_height_mm,
                box_height_mm=box_height_mm,
                box_depth_mm=box_depth_mm,
            ),
            hardware_directory=hardware_directory,
        )
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assembly": assembly_id,
                    "drawer": drawer_id,
                    "drawer_height_mm": result.plan.drawer.box.sizing.box_height_mm,
                    "drawer_side_length_mm": result.plan.drawer.box.side_length_mm,
                    "drawer_outside_depth_mm": result.plan.drawer.box.outside_depth_mm,
                    "runner_product_code": result.plan.runner.product_code,
                    "drawer_outside_width_mm": result.plan.drawer.box.outside_width_mm,
                    "recommended_width_met": (
                        result.plan.hardware_mounting.recommended_width_met
                    ),
                    "written": [str(path) for path in result.written_paths],
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
    arguments = GenerateHettichKa5332CabinetDrawerCommand.parser().parse_args()
    return GenerateHettichKa5332CabinetDrawerCommand().run(
        arguments.aikea_yaml,
        arguments.assembly,
        arguments.drawer,
        arguments.bottom_height_mm,
        arguments.box_height_mm,
        arguments.box_depth_mm,
        arguments.hardware_directory,
    )


if __name__ == "__main__":
    raise SystemExit(main())
