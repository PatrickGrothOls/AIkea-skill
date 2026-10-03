"""Scope: Provide the command that exports verified T51 device inspection CAD."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

DRAWER_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-drawers" / "scripts"
sys.path.insert(0, str(DRAWER_SCRIPTS))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError


class GenerateLockingDeviceReviewCommand:
    """Read verified local CAD and report its inspection GLB."""

    @classmethod
    def parser(cls) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Export verified Blum T51.7601 locking devices for inspection."
        )
        parser.add_argument("output", type=Path)
        parser.add_argument("--hardware-directory", required=True, type=Path)
        return parser

    def run(self, output: Path, hardware_directory: Path) -> int:
        from locking_device_review import LockingDeviceReviewGenerator

        manifest_path = (
            Path(__file__).resolve().parents[2]
            / "aikea-build-drawers"
            / "assets"
            / "blum"
            / "movento"
            / "hardware-assets.json"
        )
        result = LockingDeviceReviewGenerator(
            manifest_path,
            hardware_directory,
        ).generate(output)
        print(
            json.dumps(
                {
                    "status": "generated",
                    "glb": str(result.glb_path),
                    "assets": result.asset_ids,
                    "placement": result.placement_state,
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
    arguments = GenerateLockingDeviceReviewCommand.parser().parse_args()
    return GenerateLockingDeviceReviewCommand().run(
        arguments.output,
        arguments.hardware_directory,
    )


if __name__ == "__main__":
    raise SystemExit(main())
