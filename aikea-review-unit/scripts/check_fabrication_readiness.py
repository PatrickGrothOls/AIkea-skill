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
from fabrication_readiness_report import (
    FabricationReadinessCheck,
    FabricationReadinessReport,
)
from unit_mockup import UnitMockupInputError


class CheckFabricationReadinessCommand:
    """Build one wardrobe tree and expose every remaining fabrication blocker."""

    _ROOT_ASSEMBLY_ID = "wardrobe_01"

    def run(self, path: Path) -> int:
        output = path.parent / "manufacturing/fabrication-readiness.json"
        try:
            report = self._evaluate(path)
            report.write(output)
        # This is the single CLI boundary: any failed evaluator must revoke stale readiness.
        except Exception as error:
            problems = getattr(error, "problems", (str(error),))
            return self._invalid(output, list(problems))
        payload = report.as_dict() | {"report": str(output)}
        print(json.dumps(payload, indent=2))
        return 0 if report.is_ready else 2

    def _evaluate(self, path: Path) -> FabricationReadinessReport:
        from fabrication_readiness_gate import FabricationReadinessGate
        from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
        from project_hardware_geometry_resolver import ProjectHardwareGeometryResolver
        from purchased_hardware_hydrator import PurchasedHardwareHydrator

        project = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(project, dict):
            raise UnitMockupInputError(["aikea.yaml must contain an object"])
        loader = GeneratedAssemblyBuilderLoader()
        wardrobe = loader.load_assembly(path.parent, self._ROOT_ASSEMBLY_ID)
        wardrobe = PurchasedHardwareHydrator(ProjectHardwareGeometryResolver()).hydrate(
            path.parent,
            wardrobe,
        )
        visits = loader.walk(path.parent, wardrobe)
        return FabricationReadinessGate().evaluate(path.parent, visits)

    def _invalid(self, output: Path, problems: list[str]) -> int:
        report = FabricationReadinessReport(
            (
                FabricationReadinessCheck(
                    code="evaluation.invalid",
                    passed=False,
                    problems=tuple(problems),
                ),
            )
        )
        report.write(output)
        payload = {"status": "invalid", "problems": problems, "report": str(output)}
        print(json.dumps(payload, indent=2))
        return 2

    def invalidate(self, path: Path, problems: list[str]) -> int:
        """Revoke any saved readiness when execution cannot reach evaluation."""
        output = path.parent / "manufacturing/fabrication-readiness.json"
        return self._invalid(output, problems)


# A small function is the direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether one AIkea project is genuinely fabrication ready."
    )
    parser.add_argument("aikea_yaml", type=Path)
    arguments = parser.parse_args()
    command = CheckFabricationReadinessCommand()
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            return command.invalidate(arguments.aikea_yaml, [str(error)])
    return command.run(arguments.aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
