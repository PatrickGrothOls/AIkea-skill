"""Scope: Generate one project-owned drawer child inside an existing cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_module_renderer import CabinetDrawerModuleRenderer
from cabinet_drawer_plan import CabinetDrawerPlan, CabinetDrawerPlanner, DrawerLayout


@dataclass(frozen=True, slots=True)
class CabinetDrawerGenerationResult:
    """Report the resolved child and project files written for it."""

    plan: CabinetDrawerPlan
    written_paths: tuple[Path, ...]


class CabinetDrawerGenerator:
    """Add one drawer child without changing the overall aikea.yaml."""

    def __init__(self) -> None:
        self.spec_loader = CabinetAssemblySpecLoader()
        self.planner = CabinetDrawerPlanner()
        self.renderer = CabinetDrawerModuleRenderer()
        self.writer = AssemblyTaxonomyWriter()

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
    ) -> CabinetDrawerGenerationResult:
        cabinet = self.spec_loader.load(project_root, parent_assembly_id)
        plan = self.planner.plan(cabinet, layout)
        written = self.writer.write(project_root, self.renderer.render(plan))
        return CabinetDrawerGenerationResult(plan, written)


__all__ = ["CabinetDrawerGenerationResult", "CabinetDrawerGenerator"]
