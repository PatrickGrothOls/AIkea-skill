"""Scope: Export the structural base alone and with the first cabinet."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from cabinet_base_position_checker import CabinetBasePositionChecker
from base_mockup_geometry import BaseMockupGeometry
from base_review import BaseReviewResult
from cadquery_glb_exporter import CadQueryGlbExporter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from generated_assembly_spec_loader import GeneratedAssemblySpecLoader
from unit_mockup import UnitMockupInputError
from unit_mockup_geometry import UnitMockupGeometry


class BaseReviewGenerator:
    """Build the two visual artifacts needed to inspect the first base slice."""

    _BASE_ASSEMBLY_ID = "base_01"

    def __init__(self) -> None:
        self.loader = GeneratedAssemblyBuilderLoader()
        self.spec_loader = GeneratedAssemblySpecLoader()
        self.base_geometry = BaseMockupGeometry()
        self.cabinet_geometry = UnitMockupGeometry()
        self.position_checker = CabinetBasePositionChecker()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        project: dict[str, Any],
    ) -> BaseReviewResult:
        built_base = self.loader.load_assembly(project_root, self._BASE_ASSEMBLY_ID)
        base_parts = self.base_geometry.build(built_base)
        base_root = project_root / "assemblies" / self._BASE_ASSEMBLY_ID
        built_cabinet = self.loader.load_first(project_root, project)
        cabinet_parts = self.cabinet_geometry.build(built_cabinet)
        first_module_parts = self._first_module_parts(base_parts)
        position_report = self.position_checker.check(
            built_base,
            built_cabinet,
            base_parts,
            first_module_parts,
            cabinet_parts,
            self._next_cabinet_spec(project_root, project),
        )
        position_report_path = base_root / "assembly-position-check.json"
        position_report.write(position_report_path)
        if not position_report.is_valid:
            failed_checks = position_report.failed_check_names()
            raise UnitMockupInputError(
                ["assembly position check failed: " + ", ".join(failed_checks)]
            )

        base_glb = base_root / f"{self._BASE_ASSEMBLY_ID}.glb"
        self.exporter.export(self._BASE_ASSEMBLY_ID, base_parts, base_glb)

        combined_id = f"{built_cabinet.spec.assembly_id}_with_base"
        combined_glb = base_root / f"{combined_id}.glb"
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
            position_report_path,
        )

    def _first_module_parts(self, base_parts: tuple[Any, ...]) -> tuple[Any, ...]:
        return tuple(
            part
            for part in base_parts
            if part.name in {"deck_01", "front_rail_01", "back_rail_01"}
            or part.name.startswith("brace_01_")
        )

    def _next_cabinet_spec(
        self,
        project_root: Path,
        project: dict[str, Any],
    ) -> Any | None:
        assemblies = project["design_settings"]["assembly_run"]["assemblies"]
        if len(assemblies) < 2:
            return None
        return self.spec_loader.load(project_root, assemblies[1]["id"])


__all__ = ["BaseReviewGenerator"]
