"""Scope: Execute one generated local assembly builder without module leakage."""

from __future__ import annotations

import importlib
from pathlib import Path
import re
import sys
from typing import Any

from unit_mockup import UnitMockupInputError


class GeneratedAssemblyBuilderLoader:
    """Resolve the first ordered assembly and execute its generated builder."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def load_first(self, project_root: Path, project: dict[str, Any]) -> Any:
        assemblies = (
            project.get("design_settings", {})
            .get("assembly_run", {})
            .get("assemblies")
        )
        if not isinstance(assemblies, list) or not assemblies:
            raise UnitMockupInputError(["assembly_run must contain an ordered assembly"])
        assembly_id = assemblies[0].get("id")
        if not isinstance(assembly_id, str) or not self._ID_PATTERN.fullmatch(assembly_id):
            raise UnitMockupInputError(["the first assembly must have a stable id"])
        return self._load(project_root, assembly_id)

    def _load(self, project_root: Path, assembly_id: str) -> Any:
        builder_path = project_root / "assemblies" / assembly_id / "builder.py"
        if not builder_path.is_file():
            raise UnitMockupInputError(
                [f"missing generated local builder: {builder_path}"]
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
            module = importlib.import_module(f"assemblies.{assembly_id}.builder")
            return module.BUILDER.build()
        finally:
            sys.path.remove(str(project_root))
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
            sys.modules.update(previous)
