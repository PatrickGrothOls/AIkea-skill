"""Scope: Load one existing cabinet's generated local specification."""

from __future__ import annotations

import importlib
from pathlib import Path
import re
import sys
from typing import Any


class CabinetAssemblySpecError(ValueError):
    """Report a missing or invalid generated cabinet specification."""


class CabinetAssemblySpecLoader:
    """Read one cabinet spec without executing its geometry builder."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def load(self, project_root: Path, assembly_id: str) -> Any:
        if not self._ID_PATTERN.fullmatch(assembly_id):
            raise CabinetAssemblySpecError("the cabinet must have a stable id")
        spec_path = project_root / "assemblies" / assembly_id / "spec.py"
        if not spec_path.is_file():
            raise CabinetAssemblySpecError(
                f"missing generated cabinet specification: {spec_path}"
            )
        previous = {
            name: module
            for name, module in sys.modules.items()
            if name == "assemblies" or name.startswith("assemblies.")
        }
        for name in previous:
            sys.modules.pop(name)
        sys.path.insert(0, str(project_root))
        try:
            return importlib.import_module(f"assemblies.{assembly_id}.spec").SPEC
        finally:
            sys.path.remove(str(project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
            sys.modules.update(previous)


__all__ = ["CabinetAssemblySpecError", "CabinetAssemblySpecLoader"]
