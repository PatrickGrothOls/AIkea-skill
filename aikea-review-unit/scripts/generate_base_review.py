"""Scope: Provide the command that exports base visual-review GLBs."""

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


class GenerateBaseReviewCommand:
    """Read the project and report its two generated base-review artifacts."""

    def run(self, path: Path) -> int:
        try:
            from base_review_generator import BaseReviewGenerator

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            result = BaseReviewGenerator().generate(path.parent, project)
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
                    "base_glb": str(result.base_glb_path),
                    "cabinet_with_base_glb": str(result.cabinet_with_base_glb_path),
                    "assembly_position_check": str(result.position_report_path),
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
        description="Generate the AIkea base alone and with the first cabinet."
    )
    parser.add_argument("aikea_yaml", type=Path)
    return GenerateBaseReviewCommand().run(parser.parse_args().aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
