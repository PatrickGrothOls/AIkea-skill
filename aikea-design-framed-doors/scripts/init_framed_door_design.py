"""Scope: Install optional framed-front helpers alongside existing project contracts."""

import argparse
import json
from pathlib import Path
import sys

SKILL = Path(__file__).resolve().parents[1]
# Standalone skill commands resolve the existing sibling runtime from their own location.
sys.path.insert(0, str(SKILL.parent / "aikea-build-units/scripts"))
from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from furniture_design_project import FurnitureDesignProject


class FramedDoorDesignProject:
    def initialize(self, project_root: Path):
        contracts = FurnitureDesignProject().initialize(project_root)
        assets = SKILL / "assets/project"
        files = {Path("assemblies") / name: (assets / name).read_text()
                 for name in ("framed_front_spec.py", "applied_frame_front.py")}
        return contracts + AssemblyTaxonomyWriter().write(project_root, files)


class InitFramedDoorDesignCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("project", type=Path)
        project = parser.parse_args().project.resolve()
        paths = FramedDoorDesignProject().initialize(project)
        print(json.dumps({"project": str(project), "created": list(map(str, paths))}))


if __name__ == "__main__":
    InitFramedDoorDesignCommand().run()
