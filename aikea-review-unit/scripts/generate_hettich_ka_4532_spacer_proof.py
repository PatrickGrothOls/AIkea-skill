"""Scope: Provide the command for one exact KA 4532 spacer cabinet proof."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parents[2]
for skill_name in (
    "aikea-build-units",
    "aikea-build-drawers",
    "aikea-build-doors",
    "aikea-add-lighting",
):
    sys.path.insert(0, str(SKILL_ROOT / skill_name / "scripts"))

from cadquery_runtime import CadQueryRuntime, CadQueryRuntimeError
from generate_complete_assembly_review import FeatureStateArguments


class GenerateHettichKa4532SpacerProofCommand:
    """Create closed/open GLBs and one machine-readable physical proof."""

    def parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate one exact KA 4532 plus 13952 cabinet proof."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--output-directory", required=True, type=Path)
        parser.add_argument("--state", action="append", default=[])
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        from hettich_ka_4532_spacer_proof_generator import (
            HettichKa4532SpacerProofGenerator,
        )
        from hettich_ka_4532_spacer_proof_report import (
            HettichKa4532SpacerProofReport,
        )
        from unit_mockup import UnitMockupInputError

        report_path = (
            arguments.output_directory.resolve()
            / "ka4532-spacer-movement-collision-check.json"
        )
        try:
            result = HettichKa4532SpacerProofGenerator().generate(
                arguments.aikea_yaml.resolve().parent,
                arguments.assembly,
                arguments.output_directory.resolve(),
                FeatureStateArguments().parse(arguments.state),
            )
        except (OSError, KeyError, TypeError, UnitMockupInputError, ValueError) as error:
            HettichKa4532SpacerProofReport.invalidate(report_path, str(error))
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        payload = {
            "status": result.report.as_dict()["status"],
            "closed_glb": str(result.closed_glb_path),
            "open_glb": str(result.open_glb_path),
            "proof_report": str(result.report_path),
            "failed_checks": result.report.failed_check_names(),
        }
        print(json.dumps(payload, indent=2))
        return 0 if result.report.is_valid else 2


# This small adapter keeps runtime handoff outside the command object.
def main() -> int:
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
    command = GenerateHettichKa4532SpacerProofCommand()
    return command.run(command.parser().parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
