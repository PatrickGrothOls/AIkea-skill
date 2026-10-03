"""Scope: Initialise reusable project contracts for model-authored furniture."""

import argparse
import json
from pathlib import Path

from furniture_design_project import FurnitureDesignProject


class FurnitureDesignInitCommand:
    """Expose the contract initializer as a small local command."""

    def run(self) -> None:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        project = parser.parse_args().project.resolve()
        paths = FurnitureDesignProject().initialize(project)
        print(json.dumps({"project": str(project), "created": list(map(str, paths))}))


if __name__ == "__main__":
    FurnitureDesignInitCommand().run()
