"""Scope: Check one aikea.yaml file and print its calculated overall dimensions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

BUILD_SCRIPTS = Path(__file__).resolve().parents[2] / "aikea-build-units/scripts"
sys.path.insert(0, str(BUILD_SCRIPTS))

from assembly_run import AssemblyRunReader
from assembly_run_overall_project_adapter import AssemblyRunOverallProjectAdapter
from assembly_taxonomy import AssemblyTaxonomyInputError
from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputReader


class OverallWardrobeCommand:
    """Own the file-reading and terminal-output boundary for overall calculations."""

    def run(self, path: Path) -> int:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as error:
            print(json.dumps({"status": "invalid", "problems": [str(error)]}, indent=2))
            return 2
        try:
            project = data if isinstance(data, dict) else {}
            settings = project.get("design_settings", {})
            if isinstance(settings, dict) and "assembly_run" in settings:
                run = AssemblyRunReader().read(project)
                project = AssemblyRunOverallProjectAdapter().adapt(project, run)
            inputs = OverallWardrobeInputReader().read(project)
            result = OverallWardrobeCalculator().calculate(inputs)
        except (OverallWardrobeInputError, AssemblyTaxonomyInputError) as error:
            print(
                json.dumps(
                    {"status": "invalid", "problems": list(error.problems)}, indent=2
                )
            )
            return 2
        print(json.dumps({"status": "valid", "calculated": result.as_dict()}, indent=2))
        return 0


# A small function is the most direct adapter from Python's CLI entry point to the command object.
def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check and calculate overall AIkea wardrobe inputs."
    )
    parser.add_argument("aikea_yaml", type=Path)
    return OverallWardrobeCommand().run(parser.parse_args().aikea_yaml)


if __name__ == "__main__":
    raise SystemExit(main())
