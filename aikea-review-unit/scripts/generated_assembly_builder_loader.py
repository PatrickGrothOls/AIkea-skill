"""Scope: Execute one generated local assembly builder without module leakage."""

from __future__ import annotations

import importlib
from pathlib import Path
import re
import sys
from typing import Any, Callable

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
        return self.load_assembly(project_root, assembly_id)

    def load_assembly(
        self,
        project_root: Path,
        assembly_id: str,
        builder_module: str | None = None,
    ) -> Any:
        if not self._ID_PATTERN.fullmatch(assembly_id):
            raise UnitMockupInputError(["the assembly must have a stable id"])
        builder_module = builder_module or self._default_builder_module(
            project_root, assembly_id
        )
        if not re.fullmatch(r"[a-z][a-z0-9_]*", builder_module):
            raise UnitMockupInputError(["the builder module must have a stable name"])
        builder_path = project_root / "assemblies" / assembly_id / f"{builder_module}.py"
        if not builder_path.is_file():
            raise UnitMockupInputError(
                [f"missing generated local builder: {builder_path}"]
            )
        return self._execute(
            project_root,
            lambda: importlib.import_module(
                f"assemblies.{assembly_id}.{builder_module}"
            ).BUILDER.build(),
        )

    def walk(self, project_root: Path, built_assembly: Any) -> tuple[Any, ...]:
        """Traverse one returned assembly through its generated tree contract."""
        return self._execute(
            project_root,
            lambda: importlib.import_module(
                "assemblies.assembly_tree"
            ).AssemblyTreeWalker().walk(built_assembly),
        )

    def _execute(self, project_root: Path, operation: Callable[[], Any]) -> Any:
        previous = {
            name: module
            for name, module in sys.modules.items()
            if name == "assemblies" or name.startswith("assemblies.")
        }
        for name in previous:
            sys.modules.pop(name)
        runtime_paths = self._feature_runtime_paths()
        sys.path[:0] = [str(project_root), *runtime_paths]
        try:
            return operation()
        finally:
            for path in (str(project_root), *runtime_paths):
                sys.path.remove(path)
            for name in tuple(sys.modules):
                if name == "assemblies" or name.startswith("assemblies."):
                    sys.modules.pop(name)
            sys.modules.update(previous)

    def _default_builder_module(self, project_root: Path, assembly_id: str) -> str:
        complete = project_root / "assemblies" / assembly_id / "complete_builder.py"
        return "complete_builder" if complete.is_file() else "builder"

    def _feature_runtime_paths(self) -> tuple[str, ...]:
        skill_root = Path(__file__).resolve().parents[2]
        directories = (
            skill_root / "aikea/scripts",
            skill_root / "aikea-build-units/scripts",
            skill_root / "aikea-build-drawers/scripts",
            skill_root / "aikea-build-doors/scripts",
            skill_root / "aikea-add-lighting/scripts",
        )
        return tuple(str(path) for path in directories if path.is_dir())
