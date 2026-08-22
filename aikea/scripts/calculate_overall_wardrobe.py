"""Scope: Check one aikea.yaml file and print its calculated overall dimensions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

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
            inputs = OverallWardrobeInputReader().read(data if isinstance(data, dict) else {})
            result = OverallWardrobeCalculator().calculate(inputs)
        except OverallWardrobeInputError as error:
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
