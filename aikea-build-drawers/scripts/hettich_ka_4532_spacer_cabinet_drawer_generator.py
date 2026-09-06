"""Scope: Save one exact KA 4532 spacer drawer before repetition is allowed."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_drawer_plan import DrawerLayout
from cabinet_feature_manifest import CabinetFeatureManifest
from drawer_generated_file_record import DrawerGeneratedFileRecord
from hettich_ka_4532_spacer_cabinet_drawer_plan import (
    HettichKa4532SpacerCabinetDrawerPlan,
)
from hettich_ka_4532_spacer_cabinet_drawer_planner import (
    HettichKa4532SpacerCabinetDrawerPlanner,
)
from hettich_ka_4532_spacer_file_set_renderer import (
    HettichKa4532SpacerFileSetRenderer,
)
from hettich_ka_4532_spacer_step_set import HettichKa4532SpacerStepSetLoader
from panel_hardware_reservation import PanelHardwareReservationStore


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerDrawerGenerationResult:
    """Report the saved single-drawer proof and every changed project path."""

    plan: HettichKa4532SpacerCabinetDrawerPlan
    written_paths: tuple[Path, ...]


class HettichKa4532SpacerCabinetDrawerGenerator:
    """Generate one recursively composed cabinet without inventing machining."""

    def __init__(self, step_loader=None) -> None:
        self.specs = CabinetAssemblySpecLoader()
        self.steps = step_loader or HettichKa4532SpacerStepSetLoader()
        self.planner = HettichKa4532SpacerCabinetDrawerPlanner()
        self.renderer = HettichKa4532SpacerFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()
        self.reservations = PanelHardwareReservationStore()
        self.features = CabinetFeatureManifest()

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
        *,
        hardware_directory: Path,
        cabinet_front_mm: float,
        drawer_front_mm: float,
    ) -> HettichKa4532SpacerDrawerGenerationResult:
        cabinet = self.specs.load(project_root, parent_assembly_id)
        step_set = self.steps.load(hardware_directory)
        existing = self.reservations.load(project_root, parent_assembly_id)
        plan = self.planner.plan(
            cabinet,
            layout,
            step_set,
            existing,
            cabinet_front_mm=cabinet_front_mm,
            drawer_front_mm=drawer_front_mm,
        )
        files = self.renderer.render(plan)
        recorded = DrawerGeneratedFileRecord.load(project_root, parent_assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        DrawerGeneratedFileRecord.from_rendered(
            parent_assembly_id,
            files,
        ).save(project_root)
        reservation_path = self.reservations.write(
            project_root,
            parent_assembly_id,
            plan.hardware_reservations,
        )
        manifest = self.features.register(
            project_root,
            parent_assembly_id,
            "drawers.feature",
            10,
            review_module="drawers.review",
            affected_manufactured_part_paths=(
                "left_side",
                "right_side",
                *(f"{layout.drawer_id}/{part.part_id}" for part in plan.drawer.parts),
            ),
        )
        trailing = (reservation_path.relative_to(project_root),)
        if manifest is not None:
            trailing += (manifest.relative_to(project_root),)
        return HettichKa4532SpacerDrawerGenerationResult(
            plan,
            written + trailing,
        )


__all__ = [
    "HettichKa4532SpacerCabinetDrawerGenerator",
    "HettichKa4532SpacerDrawerGenerationResult",
]
