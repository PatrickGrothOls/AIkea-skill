"""Scope: Load one generated assembly specification without building its parts."""

from __future__ import annotations

import importlib
from pathlib import Path
import re
import sys
from typing import Any

from unit_mockup import UnitMockupInputError


class GeneratedAssemblySpecLoader:
    """Read generated position facts without producing another cabinet model."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def load(self, project_root: Path, assembly_id: str) -> Any:
        if not self._ID_PATTERN.fullmatch(assembly_id):
            raise UnitMockupInputError(["the assembly must have a stable id"])
        spec_path = project_root / "assemblies" / assembly_id / "spec.py"
        if not spec_path.is_file():
            raise UnitMockupInputError(
                [f"missing generated local specification: {spec_path}"]
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
            module = importlib.import_module(f"assemblies.{assembly_id}.spec")
            return module.SPEC
        finally:
            sys.path.remove(str(project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
            sys.modules.update(previous)


__all__ = ["GeneratedAssemblySpecLoader"]
