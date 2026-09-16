"""Scope: Select a verified installed Blender CLI or the skill-provisioned engine."""
from pathlib import Path
import shutil
import re
import subprocess
from blender_engine_runtime import BlenderEngineRuntime


class BlenderBakeRuntime:
    def command(self, runtime_directory, output_directory, threads, executable=None):
        worker = Path(__file__).with_name("run_blender_bake.py")
        runtime = BlenderEngineRuntime(runtime_directory)
        # Reuse a selected/provisioned runtime; do not duplicate a working installation.
        installed = executable or (None if runtime.python.is_file() else shutil.which("blender"))
        if installed and executable is None and not self.compatible(installed):
            installed = None
        if installed:
            # Only adapt Blender's CLI argv. The unchanged worker probes the exact
            # version, real background execution, Cycles and glTF before any bake.
            code = (f"import sys,runpy;sys.path.insert(0,{str(worker.parent)!r});"
                    f"sys.argv=[{str(worker)!r},{str(output_directory)!r}];"
                    f"runpy.run_path({str(worker)!r},run_name='__main__')")
            return [str(installed), "--background", "--factory-startup", "--threads", str(threads),
                    "--python-exit-code", "1", "--python-expr", code]
        return [str(runtime.ensure()), str(worker), str(output_directory)]

    def compatible(self, executable):
        # Version mismatch is recoverable; a failed process remains an explicit
        # execution problem, not a reason to download another large runtime.
        result = subprocess.run([str(executable), "--version"], check=True,
                                capture_output=True, text=True)
        match = re.search(r"^Blender (\d+\.\d+\.\d+)\b", result.stdout, re.MULTILINE)
        if match is None:
            raise ValueError("Installed Blender returned no recognizable version")
        return match.group(1) == BlenderEngineRuntime.VERSION
