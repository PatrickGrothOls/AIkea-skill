"""Scope: Check or install a package-local, pinned AIkea CAD runtime."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import venv


class PortableRuntime:
    """Keep optional dependency installation inside the extracted package."""

    def __init__(self, root: Path) -> None:
        self.root = root
        if sys.version_info[:2] not in {(3, 10), (3, 11), (3, 12)} or sys.platform not in {"darwin", "linux"}:
            raise SystemExit("CAD setup requires Python 3.10–3.12 on macOS or Linux; guided intake remains available.")

    def prepare(self, install: bool) -> None:
        interpreter = Path(sys.executable).absolute()
        if install:
            environment = self.root / ".venv"
            if not environment.exists():
                venv.EnvBuilder(with_pip=True).create(environment)
            interpreter = environment / "bin" / "python"
            subprocess.run(
                [str(interpreter), "-m", "pip", "install", "-r", str(self.root / "requirements.txt")],
                check=True,
            )
        subprocess.run(
            [str(interpreter), str(self.root / "setup_aikea.py"), "--probe"], check=True
        )
        print(f"AIKEA_CADQUERY_PYTHON={interpreter}")

    def probe(self) -> None:
        import cadquery as cq
        import vtk
        import yaml

        expected = {"cadquery": "2.7.0", "vtk": "9.3.1", "PyYAML": "6.0.2"}
        actual = {"cadquery": cq.__version__, "vtk": vtk.vtkVersion.GetVTKVersion(), "PyYAML": yaml.__version__}
        if actual != expected:
            raise SystemExit(f"Dependency versions differ: {json.dumps(actual)}; use --install.")
        solid = cq.Workplane("XY").box(1, 2, 3).val()
        if not solid.isValid() or abs(solid.Volume() - 6) > 1e-8:
            raise SystemExit("CadQuery solid check failed.")
        print("CAD runtime verified: " + json.dumps(actual, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="Install into this package's .venv")
    parser.add_argument("--probe", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    runtime = PortableRuntime(Path(__file__).resolve().parent)
    if args.probe:
        runtime.probe()
    else:
        runtime.prepare(args.install)
