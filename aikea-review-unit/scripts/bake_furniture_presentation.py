"""Scope: Provision Blender and create a checked assembled presentation from a material GLB."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from blender_engine_runtime import BlenderEngineRuntime


class FurniturePresentationCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("source", type=Path)
        parser.add_argument("output_directory", type=Path, help="New directory for this immutable bake")
        parser.add_argument("--runtime-directory", type=Path, required=True)
        parser.add_argument("--units", choices=("mm", "m"), default="mm")
        parser.add_argument("--atlas-size", type=int, choices=(512, 1024, 2048, 4096), default=4096)
        parser.add_argument("--threads", type=int, choices=range(1, 5), default=3)
        parser.add_argument("--samples", type=int, choices=(1, 8, 16, 32, 64), default=16)
        args = parser.parse_args()
        source = args.source.resolve(strict=True)
        output = args.output_directory.resolve()
        output.mkdir(parents=True, exist_ok=False)
        config = {"source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                  "unit_scale": 0.001 if args.units == "mm" else 1.0,
                  "atlas_size": args.atlas_size, "threads": args.threads, "samples": args.samples}
        (output / "job.json").write_text(json.dumps(config, indent=2))
        python = BlenderEngineRuntime(args.runtime_directory).ensure()
        worker = Path(__file__).with_name("run_blender_bake.py")
        with (output / "bake.log").open("w") as log:
            subprocess.run([str(python), str(worker), str(output)], stdout=log,
                           stderr=subprocess.STDOUT, check=True)
        print((output / "presentation.json").read_text())


if __name__ == "__main__":
    FurniturePresentationCommand().run()
