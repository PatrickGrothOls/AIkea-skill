"""Scope: Provide the command that generates one cabinet-owned drawer child."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units" / "scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from cabinet_drawer_generator import CabinetDrawerGenerator
from cabinet_drawer_plan import DrawerLayout


class GenerateCabinetDrawerCommand:
    """Create the local drawer layout, child builder, and parent composition."""

    def run(
        self,
        aikea_yaml: Path,
        assembly_id: str,
        drawer_id: str,
        bottom_height_mm: float,
    ) -> int:
        result = CabinetDrawerGenerator().generate(
            aikea_yaml.parent,
            assembly_id,
            DrawerLayout(drawer_id, bottom_height_mm),
        )
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assembly": assembly_id,
                    "drawer": drawer_id,
                    "runner_product_code": result.plan.runner.product_code,
                    "written": [str(path) for path in result.written_paths],
                },
                indent=2,
            )
        )
        return 0


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one AIkea cabinet drawer.")
    parser.add_argument("aikea_yaml", type=Path)
    parser.add_argument("--assembly", required=True)
    parser.add_argument("--drawer", default="drawer_01")
    parser.add_argument("--bottom-height-mm", required=True, type=float)
    arguments = parser.parse_args()
    return GenerateCabinetDrawerCommand().run(
        arguments.aikea_yaml,
        arguments.assembly,
        arguments.drawer,
        arguments.bottom_height_mm,
    )


if __name__ == "__main__":
    raise SystemExit(main())
