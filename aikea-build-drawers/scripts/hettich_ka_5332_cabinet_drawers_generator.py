"""Scope: Save any number of independent KA 5332 drawers in one cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_plan import DrawerLayout
from cabinet_feature_manifest import CabinetFeatureManifest
from drawer_generated_file_record import DrawerGeneratedFileRecord
from hettich_ka_5332_cabinet_drawers_plan import (
    HettichKa5332CabinetDrawersPlan,
    HettichKa5332CabinetDrawersPlanner,
)
from hettich_ka_5332_drawer_layout_collection_loader import (
    HettichKa5332DrawerLayoutCollectionLoader,
)
from hettich_ka_5332_drawers_file_set_renderer import (
    HettichKa5332DrawersFileSetRenderer,
)
from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader
from panel_hardware_reservation import PanelHardwareReservationStore


@dataclass(frozen=True, slots=True)
class HettichKa5332DrawersGenerationResult:
    """Report the complete saved collection and its changed project files."""

    plan: HettichKa5332CabinetDrawersPlan
    written_paths: tuple[Path, ...]


class HettichKa5332CabinetDrawersGenerator:
    """Generate or revise independently sized and positioned drawer children."""

    def __init__(self, step_loader=None) -> None:
        self.spec_loader = CabinetAssemblySpecLoader()
        self.step_loader = step_loader or HettichKa5332StepAssemblyLoader()
        self.layout_loader = HettichKa5332DrawerLayoutCollectionLoader()
        self.planner = HettichKa5332CabinetDrawersPlanner()
        self.renderer = HettichKa5332DrawersFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()
        self.reservation_store = PanelHardwareReservationStore()
        self.features = CabinetFeatureManifest()

    def add(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
        *,
        hardware_directory: Path,
    ) -> HettichKa5332DrawersGenerationResult:
        existing = self.layout_loader.load(project_root, parent_assembly_id)
        layouts = self._upsert(existing, layout)
        return self.generate(
            project_root,
            parent_assembly_id,
            layouts,
            hardware_directory=hardware_directory,
        )

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layouts: tuple[DrawerLayout, ...],
        *,
        hardware_directory: Path,
    ) -> HettichKa5332DrawersGenerationResult:
        cabinet = self.spec_loader.load(project_root, parent_assembly_id)
        hardware_step = self.step_loader.load(hardware_directory)
        existing = tuple(
            item
            for item in self.reservation_store.load(
                project_root,
                parent_assembly_id,
            )
            if item.hardware_kind != "drawer_runner"
        )
        plan = self.planner.plan(
            cabinet,
            layouts,
            hardware_step,
            existing,
        )
        files = self.renderer.render(plan)
        recorded = DrawerGeneratedFileRecord.load(project_root, parent_assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        DrawerGeneratedFileRecord.from_rendered(
            parent_assembly_id,
            files,
        ).save(project_root)
        reservation_path = self.reservation_store.write(
            project_root,
            parent_assembly_id,
            plan.hardware_reservations,
        )
        manifest_path = self.features.register(
            project_root,
            parent_assembly_id,
            "drawers.feature",
            10,
            affected_manufactured_part_paths=(
                "left_side",
                "right_side",
                *(
                    f"{drawer.drawer.assembly_id}/{part.part_id}"
                    for drawer in plan.drawers
                    for part in drawer.drawer.parts
                ),
            ),
        )
        return HettichKa5332DrawersGenerationResult(
            plan,
            written
            + (
                reservation_path.relative_to(project_root),
                *(
                    (manifest_path.relative_to(project_root),)
                    if manifest_path
                    else ()
                ),
            ),
        )

    def _upsert(
        self,
        layouts: tuple[DrawerLayout, ...],
        replacement: DrawerLayout,
    ) -> tuple[DrawerLayout, ...]:
        if any(layout.drawer_id == replacement.drawer_id for layout in layouts):
            return tuple(
                replacement if layout.drawer_id == replacement.drawer_id else layout
                for layout in layouts
            )
        return layouts + (replacement,)


__all__ = [
    "HettichKa5332CabinetDrawersGenerator",
    "HettichKa5332DrawersGenerationResult",
]
