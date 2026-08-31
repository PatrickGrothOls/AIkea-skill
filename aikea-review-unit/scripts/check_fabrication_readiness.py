"""Scope: Evaluate and write the complete recursive fabrication-readiness gate."""

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


class CheckFabricationReadinessCommand:
    """Build one wardrobe tree and expose every remaining fabrication blocker."""

    _ROOT_ASSEMBLY_ID = "wardrobe_01"

    def run(self, path: Path) -> int:
        try:
            from fabrication_readiness_gate import FabricationReadinessGate
            from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader

            project = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(project, dict):
                raise UnitMockupInputError(["aikea.yaml must contain an object"])
            loader = GeneratedAssemblyBuilderLoader()
            wardrobe = loader.load_assembly(path.parent, self._ROOT_ASSEMBLY_ID)
            visits = loader.walk(path.parent, wardrobe)
            report = FabricationReadinessGate().evaluate(path.parent, visits)
            output = path.parent / "manufacturing/fabrication-readiness.json"
            report.write(output)
        except (OSError, yaml.YAMLError, PartConstructionError) as error:
            return self._invalid([str(error)])
        except UnitMockupInputError as error:
            return self._invalid(list(error.problems))
        payload = report.as_dict() | {"report": str(output)}
        print(json.dumps(payload, indent=2))
        return 0 if report.is_ready else 2

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
        description="Check whether one AIkea project is genuinely fabrication ready."
    )
    parser.add_argument("aikea_yaml", type=Path)
    return CheckFabricationReadinessCommand().run(parser.parse_args().aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
