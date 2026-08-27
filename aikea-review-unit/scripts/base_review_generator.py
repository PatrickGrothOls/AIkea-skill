"""Scope: Export the structural base alone and with the first cabinet."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from base_mockup_geometry import BaseMockupGeometry
from base_review import BaseReviewResult
from cadquery_glb_exporter import CadQueryGlbExporter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from unit_mockup_geometry import UnitMockupGeometry


class BaseReviewGenerator:
    """Build the two visual artifacts needed to inspect the first base slice."""

    _BASE_ASSEMBLY_ID = "base_01"

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.base_geometry = BaseMockupGeometry()
        self.cabinet_geometry = UnitMockupGeometry()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
    ) -> BaseReviewResult:
        built_base = self.loader.load_assembly(project_root, self._BASE_ASSEMBLY_ID)
        base_parts = self.base_geometry.build(built_base)
        base_root = project_root / "assemblies" / self._BASE_ASSEMBLY_ID
        base_glb = base_root / f"{self._BASE_ASSEMBLY_ID}.glb"
        self.exporter.export(self._BASE_ASSEMBLY_ID, base_parts, base_glb)

        built_cabinet = self.loader.load_first(project_root, project)
        cabinet_parts = self.cabinet_geometry.build(built_cabinet)
        combined_id = f"{built_cabinet.spec.assembly_id}_with_base"
        combined_glb = base_root / f"{combined_id}.glb"
        first_module_parts = self._first_module_parts(base_parts)
        self.exporter.export(
            combined_id,
            (*first_module_parts, *cabinet_parts),
            combined_glb,
        )
        return BaseReviewResult(
            built_base.spec.assembly_id,
            built_cabinet.spec.assembly_id,
            base_glb,
            combined_glb,
        )

    def _first_module_parts(self, base_parts: tuple[Any, ...]) -> tuple[Any, ...]:
        return tuple(
            part
            for part in base_parts
            if part.name.endswith("_01") or part.name.startswith("brace_01_")
        )


__all__ = ["BaseReviewGenerator"]
