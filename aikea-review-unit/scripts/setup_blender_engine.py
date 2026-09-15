"""Scope: Install the skill's required Blender engine without a desktop UI."""

import argparse
from pathlib import Path
from blender_engine_runtime import BlenderEngineRuntime


class BlenderSetupCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("runtime_directory", type=Path)
        args = parser.parse_args()
        print(BlenderEngineRuntime(args.runtime_directory).ensure())


if __name__ == "__main__":
    BlenderSetupCommand().run()
