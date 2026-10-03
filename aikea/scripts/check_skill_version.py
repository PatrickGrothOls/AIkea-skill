"""Scope: Run the read-only skill release check with the standard Python library."""

import argparse
import json
from pathlib import Path

from skill_release_check import SkillReleaseCheck


class CheckSkillVersionCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--metadata", type=Path, default=Path(__file__).resolve().parents[1]/"release.json")
        arguments = parser.parse_args()
        print(json.dumps(SkillReleaseCheck().check(arguments.metadata), indent=2))


if __name__ == "__main__":
    CheckSkillVersionCommand().run()
