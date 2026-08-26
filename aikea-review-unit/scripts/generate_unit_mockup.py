"""Scope: Provide the terminal command that generates the first cabinet mock-up."""

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


class GenerateUnitMockupCommand:
    """Read one project file and report its generated visual-review artifact."""

    def run(self, path: Path) -> int:
        try:
            from unit_mockup_generator import UnitMockupGenerator

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            result = UnitMockupGenerator().generate_first(path.parent, project)
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
                    "assembly_id": result.assembly_id,
                    "glb": str(result.glb_path),
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
        description="Generate the first AIkea cabinet as a visual GLB mock-up."
    )
    parser.add_argument("aikea_yaml", type=Path)
    return GenerateUnitMockupCommand().run(parser.parse_args().aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
