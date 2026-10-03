"""Scope: Provision and verify the isolated Blender Python engine used by the skill."""

import os
from pathlib import Path
import shutil
import subprocess
import sys


class BlenderEngineRuntime:
    VERSION = "5.2.1"
    PYTHON = "3.13"
    UV_VERSION = "0.7.3"

    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.environment = self.directory / f"bpy-{self.VERSION}"
        self.python = self.environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

    def uv_command(self):
        available = shutil.which("uv")
        if available:
            return [available]
        bootstrap = self.directory / "bootstrap"
        subprocess.run([sys.executable, "-m", "pip", "install", "--only-binary=:all:",
                        "--index-url", "https://pypi.org/simple", "--target", str(bootstrap),
                        f"uv=={self.UV_VERSION}"], check=True)
        # uv's wheel carries its binary; no system installation or shell profile edit.
        executable = next(path for path in bootstrap.rglob("uv.exe" if os.name == "nt" else "uv")
                          if path.is_file())
        return [str(executable)]

    def ensure(self):
        self.directory.mkdir(parents=True, exist_ok=True)
        env = dict(os.environ, UV_CACHE_DIR=str(self.directory / "cache"),
                   UV_PYTHON_INSTALL_DIR=str(self.directory / "python"))
        if not self.python.is_file():
            uv = self.uv_command()
            subprocess.run(uv + ["venv", "--python", self.PYTHON, "--managed-python",
                                 str(self.environment)], env=env, check=True)
        probe = subprocess.run([str(self.python), "-c",
                                "import bpy; print('.'.join(map(str, bpy.app.version)))"],
                               text=True, capture_output=True)
        if probe.returncode != 0 or probe.stdout.strip() != self.VERSION:
            subprocess.run(self.uv_command() + ["pip", "install", "--python", str(self.python),
                           "--index-url", "https://pypi.org/simple", "--only-binary=:all:",
                           f"bpy=={self.VERSION}"], env=env, check=True)
        subprocess.run([str(self.python), str(Path(__file__).with_name("probe_blender_engine.py"))],
                       check=True)
        return self.python
