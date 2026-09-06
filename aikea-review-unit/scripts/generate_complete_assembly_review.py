"""Scope: Provide the CLI for one generic recursively composed assembly review."""

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


class FeatureStateArguments:
    """Parse stable assembly/feature selectors without furniture assumptions."""

    def parse(self, values: list[str]) -> dict[str, str]:
        states = {}
        for value in values:
            selector, separator, state = value.partition("=")
            if not separator or "/" not in selector or not state:
                raise ValueError(
                    "feature state must use <assembly-id>/<feature-id>=<state>"
                )
            if selector in states:
                raise ValueError(f"duplicate feature state: {selector}")
            states[selector] = state
        return states


class GenerateCompleteAssemblyReviewCommand:
    """Run the reusable tree review and print its exact artifact contract."""

    def parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Generate one complete recursive assembly GLB."
        )
        parser.add_argument("aikea_yaml", type=Path)
        parser.add_argument("--assembly", required=True)
        parser.add_argument("--output", required=True, type=Path)
        parser.add_argument("--state", action="append", default=[])
        return parser

    def run(self, arguments: argparse.Namespace) -> int:
        from complete_assembly_review_generator import CompleteAssemblyReviewGenerator
        from unit_mockup import UnitMockupInputError

        try:
            states = FeatureStateArguments().parse(arguments.state)
            result = CompleteAssemblyReviewGenerator().generate(
                arguments.aikea_yaml.resolve().parent,
                arguments.assembly,
                arguments.output.resolve(),
                states,
            )
        except (UnitMockupInputError, ValueError) as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
        print(
            json.dumps(
                {
                    "status": "generated-for-visual-approval",
                    "assembly_id": result.assembly_id,
                    "glb": str(result.glb_path),
                    "part_count": result.part_count,
                    "feature_selectors": result.feature_selectors,
                    "review_report": str(result.report_path),
                },
                indent=2,
            )
        )
        return 0


# This small adapter keeps runtime handoff outside the command object.
def main() -> int:
    runtime = CadQueryRuntime.from_environment()
    if not runtime.current_is_ready():
        try:
            return runtime.run_script(Path(__file__).resolve(), sys.argv[1:])
        except CadQueryRuntimeError as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}))
            return 2
    return GenerateCompleteAssemblyReviewCommand().run(
        GenerateCompleteAssemblyReviewCommand().parser().parse_args()
    )


if __name__ == "__main__":
    raise SystemExit(main())
