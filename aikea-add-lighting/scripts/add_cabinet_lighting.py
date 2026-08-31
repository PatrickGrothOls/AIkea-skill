"""Scope: Provide the terminal command that saves one cabinet light plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [
    str(SKILL_ROOT / "aikea-build-units/scripts"),
    str(SKILL_ROOT / "aikea-build-drawers/scripts"),
]

from cabinet_lighting_generator import CabinetLightingGenerator
from lighting_run import LightingRun
from recessed_luminaire_profile import DOMUS_APEX_84_HI


class AddCabinetLightingCommand:
    """Save one explicit host-part run and report its generated files."""

    def run(self, arguments: argparse.Namespace) -> int:
        run = LightingRun(
            arguments.run_id,
            tuple(arguments.start),
            tuple(arguments.end),
            arguments.color_temperature,
            DOMUS_APEX_84_HI,
        )
        result = CabinetLightingGenerator().generate(
            arguments.aikea_yaml.parent,
            arguments.assembly_id,
            arguments.part_id,
            run,
            base_builder_module=arguments.base_builder_module,
        )
        print(
            json.dumps(
                {
                    "status": "generated",
                    "assembly_id": result.plan.assembly_id,
                    "part_id": result.plan.part_id,
                    "written_paths": [str(path) for path in result.written_paths],
                },
                indent=2,
            )
        )
        return 0


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Save one recessed light in an existing generated cabinet."
    )
    parser.add_argument("aikea_yaml", type=Path)
    parser.add_argument("--assembly-id", required=True)
    parser.add_argument("--part-id", required=True)
    parser.add_argument("--base-builder-module", default="builder")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--start", nargs=2, type=float, required=True)
    parser.add_argument("--end", nargs=2, type=float, required=True)
    parser.add_argument("--color-temperature", type=int, default=3200)
    try:
        return AddCabinetLightingCommand().run(parser.parse_args())
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "invalid", "problems": [str(error)]}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
