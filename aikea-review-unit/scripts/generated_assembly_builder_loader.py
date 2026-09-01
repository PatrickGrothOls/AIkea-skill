"""Scope: Execute one generated local assembly builder without module leakage."""

from __future__ import annotations

import importlib
from pathlib import Path
import re
from typing import Any

from generated_project_module_runtime import GeneratedProjectModuleRuntime
from unit_mockup import UnitMockupInputError


class GeneratedAssemblyBuilderLoader:
    """Resolve the first ordered assembly and execute its generated builder."""

    _ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*_[0-9]{2}$")

    def __init__(self, runtime: GeneratedProjectModuleRuntime | None = None) -> None:
        self.runtime = runtime or GeneratedProjectModuleRuntime()

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
        return self.runtime.execute(
            project_root,
            lambda: importlib.import_module(
                f"assemblies.{assembly_id}.{builder_module}"
            ).BUILDER.build(),
        )

    def walk(self, project_root: Path, built_assembly: Any) -> tuple[Any, ...]:
        """Traverse one returned assembly through its generated tree contract."""
        return self.runtime.execute(
            project_root,
            lambda: importlib.import_module(
                "assemblies.assembly_tree"
            ).AssemblyTreeWalker().walk(built_assembly),
        )

    def _default_builder_module(self, project_root: Path, assembly_id: str) -> str:
        complete = project_root / "assemblies" / assembly_id / "complete_builder.py"
        return "complete_builder" if complete.is_file() else "builder"
