"""Scope: Generate one project-owned drawer child inside an existing cabinet."""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from cabinet_assembly_spec_loader import CabinetAssemblySpecLoader
from cabinet_feature_manifest import CabinetFeatureManifest
from cabinet_drawer_file_set_renderer import CabinetDrawerFileSetRenderer
from cabinet_drawer_plan import CabinetDrawerPlan, CabinetDrawerPlanner, DrawerLayout
from drawer_hardware_set_verifier import DrawerHardwareSetVerifierFactory
from drawer_generated_file_record import DrawerGeneratedFileRecord


@dataclass(frozen=True, slots=True)
class CabinetDrawerGenerationResult:
    """Report the resolved child and project files written for it."""

    plan: CabinetDrawerPlan
    written_paths: tuple[Path, ...]


class CabinetDrawerGenerator:
    """Add one drawer child without changing the overall aikea.yaml."""

    def __init__(
        self,
        hardware_verifier_factory: DrawerHardwareSetVerifierFactory | None = None,
    ) -> None:
        self.spec_loader = CabinetAssemblySpecLoader()
        self.planner = CabinetDrawerPlanner()
        self.renderer = CabinetDrawerFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()
        self.features = CabinetFeatureManifest()
        self.hardware_verifier_factory = (
            hardware_verifier_factory or DrawerHardwareSetVerifierFactory()
        )

    def generate(
        self,
        project_root: Path,
        parent_assembly_id: str,
        layout: DrawerLayout,
        *,
        hardware_directory: Path,
    ) -> CabinetDrawerGenerationResult:
        cabinet = self.spec_loader.load(project_root, parent_assembly_id)
        plan = self.planner.plan(cabinet, layout)
        hardware = self.hardware_verifier_factory.create(hardware_directory).verify(
            plan.runner
        )
        plan = replace(
            plan,
            drawer=replace(
                plan.drawer,
                hardware_geometry_state=plan.hardware_mounting.geometry_state,
            ),
        )
        files = self.renderer.render(plan)
        recorded = DrawerGeneratedFileRecord.load(project_root, parent_assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        DrawerGeneratedFileRecord.from_rendered(
            parent_assembly_id,
            files,
        ).save(project_root)
        manifest = self.features.register(
            project_root,
            parent_assembly_id,
            "drawers.feature",
            10,
            affected_manufactured_part_paths=tuple(
                f"{plan.drawer.assembly_id}/{part.part_id}"
                for part in plan.drawer.parts
            ),
        )
        return CabinetDrawerGenerationResult(
            plan,
            written
            + ((manifest.relative_to(project_root),) if manifest else ()),
        )


__all__ = ["CabinetDrawerGenerationResult", "CabinetDrawerGenerator"]
