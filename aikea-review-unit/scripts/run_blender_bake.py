"""Scope: Run one bake job inside the provisioned background Blender engine."""

import sys
from pathlib import Path
from blender_bake_job import BlenderBakeJob
from probe_blender_engine import BlenderEngineProbe


class BlenderBakeWorker:
    def run(self):
        BlenderEngineProbe().run()
        BlenderBakeJob(Path(sys.argv[1]).resolve()).run()


if __name__ == "__main__":
    BlenderBakeWorker().run()
