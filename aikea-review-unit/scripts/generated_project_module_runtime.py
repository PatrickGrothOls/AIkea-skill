"""Scope: Execute project-generated assembly modules without import leakage."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Callable


class GeneratedProjectModuleRuntime:
    """Temporarily expose one generated project and restore prior imports."""

    def execute(self, project_root: Path, operation: Callable[[], Any]) -> Any:
        previous = {
            name: module
            for name, module in sys.modules.items()
            if name == "assemblies" or name.startswith("assemblies.")
        }
        for name in previous:
            sys.modules.pop(name)
        runtime_paths = self._skill_runtime_paths()
        inserted_paths = (str(project_root), *runtime_paths)
        sys.path[:0] = list(inserted_paths)
        try:
            return operation()
        finally:
            for path in inserted_paths:
                sys.path.remove(path)
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
            sys.modules.update(previous)

    def _skill_runtime_paths(self) -> tuple[str, ...]:
        skill_root = Path(__file__).resolve().parents[2]
        directories = (
            skill_root / "aikea/scripts",
            skill_root / "aikea-build-units/scripts",
            skill_root / "aikea-build-drawers/scripts",
            skill_root / "aikea-build-doors/scripts",
            skill_root / "aikea-add-lighting/scripts",
        )
        return tuple(str(path) for path in directories if path.is_dir())


__all__ = ["GeneratedProjectModuleRuntime"]
