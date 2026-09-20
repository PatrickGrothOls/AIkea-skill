"""Scope: Install isolated CAD/Blender dependencies and run the packaged runtime proof."""

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import uuid

from package_integrity import PackageIntegrity
from setup_report import SetupReport, SetupStepFailure


class DesktopSetup:
    def run(self, root, runtime, uv):
        identity = PackageIntegrity().verify(root)
        if shutil.disk_usage(runtime).free < 4 * 1024**3:
            raise ValueError("Setup needs 4 GiB free for installation and test artifacts; free space and retry.")
        report = SetupReport(runtime / "attempts" / uuid.uuid4().hex, identity)
        env = dict(os.environ, UV_PYTHON_INSTALL_DIR=str(runtime / "python"),
                   UV_CACHE_DIR=str(runtime / "cache"), UV_NO_CONFIG="1",
                   UV_LINK_MODE="copy", PATH=f"{uv.parent}:/usr/bin:/bin:/usr/sbin:/sbin")
        for name in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV", "AIKEA_CADQUERY_PYTHON"):
            env.pop(name, None)
        cad = str(runtime / "cad/bin/python")
        report.run("cad_dependencies", [str(uv), "--no-config", "pip", "install", "--python", cad,
                   "--index-url", "https://pypi.org/simple", "--only-binary", ":all:",
                   "-r", str(root / "requirements.txt")], env)
        report.run("cad_probe", [cad, str(root / "probe_cad.py"), str(report.directory),
                                  str(root)], env)
        review = root / "skills/aikea-review-unit/scripts"
        report.run("blender_dependencies", [cad, str(review / "setup_blender_engine.py"),
                                             str(runtime / "blender")], env)
        engine = str(runtime / "blender/bpy-5.2.1/bin/python")
        report.run("blender_bake", [engine, str(root / "probe_presentation.py"),
                                    str(report.directory), str(root)], env)
        presentation = report.directory / "presentation/assembled.glb"
        report.complete({"cad": cad, "blender": engine},
                        {"step": str(report.directory / "probe.step"),
                         "inspection": str(report.directory / "probe.glb"),
                         "presentation": str(presentation)})


class SetupCommand:
    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--runtime-directory", type=Path, required=True)
        parser.add_argument("--uv", type=Path, required=True)
        args = parser.parse_args()
        try:
            DesktopSetup().run(Path(__file__).resolve().parent,
                               args.runtime_directory.resolve(), args.uv.resolve())
        except (SetupStepFailure, OSError, ValueError) as error:
            # CLI boundary reports known filesystem, package and child-process failures.
            print(json.dumps({"status": "BLOCKED", "error": str(error)}), file=sys.stderr)
            raise SystemExit(1) from error


if __name__ == "__main__":
    SetupCommand().run()
