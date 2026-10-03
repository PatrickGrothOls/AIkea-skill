"""Scope: Provide the CLI for the first exact AIkea door-and-hinge proof."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

import yaml

SKILL_ROOT = Path(__file__).resolve().parents[2]
AIKEA_SCRIPTS = SKILL_ROOT / "aikea" / "scripts"
BUILD_SCRIPTS = SKILL_ROOT / "aikea-build-units" / "scripts"
REVIEW_SCRIPTS = SKILL_ROOT / "aikea-review-unit" / "scripts"
for scripts in (AIKEA_SCRIPTS, BUILD_SCRIPTS, REVIEW_SCRIPTS):
    sys.path.insert(0, str(scripts))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError


class GenerateDoorHingeReviewCommand:
    """Read one saved project and emit its exact hinge proof artifacts."""

    def run(
        self,
        aikea_yaml: Path,
        assembly_id: str,
        hardware_root: Path,
    ) -> int:
        from cabinet_door_hinge_review_generator import (
            CabinetDoorHingeReviewGenerator,
        )

        project = yaml.safe_load(aikea_yaml.read_text(encoding="utf-8"))
        result = CabinetDoorHingeReviewGenerator().generate(
            aikea_yaml.parent,
            project,
            assembly_id,
            hardware_root,
        )
        values = asdict(result)
        values["status"] = "generated"
        values = {
            key: str(value) if isinstance(value, Path) else value
            for key, value in values.items()
        }
        print(json.dumps(values, indent=2))
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
        description="Generate one cabinet with exact closed and open hinge CAD."
    )
    parser.add_argument("aikea_yaml", type=Path)
    parser.add_argument("--assembly", required=True)
    parser.add_argument("--hardware-root", required=True, type=Path)
    arguments = parser.parse_args()
    return GenerateDoorHingeReviewCommand().run(
        arguments.aikea_yaml,
        arguments.assembly,
        arguments.hardware_root,
    )


if __name__ == "__main__":
    raise SystemExit(main())
