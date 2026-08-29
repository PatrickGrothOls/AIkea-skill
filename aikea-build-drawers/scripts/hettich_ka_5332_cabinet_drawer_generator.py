"""Scope: Save one KA 5332 drawer child beneath an existing cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_plan import DrawerLayout
from drawer_generated_file_record import DrawerGeneratedFileRecord
from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
    HettichKa5332CabinetDrawerPlanner,
)
from hettich_ka_5332_drawer_file_set_renderer import (
    HettichKa5332DrawerFileSetRenderer,
)
from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader


@dataclass(frozen=True, slots=True)
class HettichKa5332DrawerGenerationResult:
    """Report the saved drawer plan and project files written for it."""

    plan: HettichKa5332CabinetDrawerPlan
    written_paths: tuple[Path, ...]


class HettichKa5332CabinetDrawerGenerator:
    """Generate the wooden child only after exact source CAD resolves."""

    def __init__(
        self,
        step_loader: HettichKa5332StepAssemblyLoader | None = None,
    ) -> None:
        self.spec_loader = CabinetAssemblySpecLoader()
        self.step_loader = step_loader or HettichKa5332StepAssemblyLoader()
        self.planner = HettichKa5332CabinetDrawerPlanner()
        self.renderer = HettichKa5332DrawerFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
        *,
        hardware_directory: Path,
    ) -> HettichKa5332DrawerGenerationResult:
        cabinet = self.spec_loader.load(project_root, parent_assembly_id)
        hardware_step = self.step_loader.load(hardware_directory)
        plan = self.planner.plan(cabinet, layout, hardware_step)
        files = self.renderer.render(plan)
        recorded = DrawerGeneratedFileRecord.load(project_root, parent_assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        DrawerGeneratedFileRecord.from_rendered(
            parent_assembly_id,
            files,
        ).save(project_root)
        return HettichKa5332DrawerGenerationResult(plan, written)


__all__ = [
    "HettichKa5332CabinetDrawerGenerator",
    "HettichKa5332DrawerGenerationResult",
]
