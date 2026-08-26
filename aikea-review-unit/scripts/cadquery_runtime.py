"""Scope: Locate and launch the project's existing CadQuery Python runtime."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import sys


class CadQueryRuntimeError(RuntimeError):
    """Report that no usable CadQuery interpreter is available."""


class CadQueryRuntime:
    """Keep CadQuery environment discovery behind one reusable command boundary."""

    def __init__(
        self,
        current_python: Path,
        environment_roots: tuple[Path, ...],
        override: Path | None,
    ) -> None:
        self.current_python = current_python.resolve()
        self.environment_roots = environment_roots
        self.override = override

    @classmethod
    def from_environment(cls) -> "CadQueryRuntime":
        roots = {Path(sys.prefix).resolve()}
        conda_executable = os.environ.get("CONDA_EXE")
        if conda_executable:
            roots.add(Path(conda_executable).resolve().parent.parent)
        override_value = os.environ.get("AIKEA_CADQUERY_PYTHON")
        override = Path(override_value).expanduser() if override_value else None
        return cls(Path(sys.executable), tuple(sorted(roots)), override)

    def current_is_ready(self) -> bool:
        return importlib.util.find_spec("cadquery") is not None

    def run_script(self, script: Path, arguments: list[str]) -> int:
        interpreter = self.resolve()
        completed = subprocess.run([str(interpreter), str(script), *arguments])
        return completed.returncode

    def resolve(self) -> Path:
        for candidate in self._candidates():
            if candidate.is_file() and self._supports_cadquery(candidate):
                return candidate
        raise CadQueryRuntimeError(
            "No CadQuery Python runtime was found. Set AIKEA_CADQUERY_PYTHON to its interpreter."
        )

    def _candidates(self) -> tuple[Path, ...]:
        candidates = [self.override, self.current_python]
        for root in self.environment_roots:
            environments = root / "envs"
            if environments.is_dir():
                candidates.extend(
                    self._environment_python(environment)
                    for environment in sorted(environments.iterdir())
                )
        return tuple(candidate.resolve() for candidate in candidates if candidate)

    def _environment_python(self, environment: Path) -> Path:
        posix_python = environment / "bin" / "python"
        return posix_python if posix_python.is_file() else environment / "python.exe"

    def _supports_cadquery(self, interpreter: Path) -> bool:
        result = subprocess.run(
            [str(interpreter), "-c", "import cadquery"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
