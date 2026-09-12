"""Scope: Save one recessed-light plan into an existing generated cabinet."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from assembly_taxonomy_writer import AssemblyTaxonomyWriter
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from lighting_machining_recipe import LightingMachiningRecipe
from lighting_component_feature import LightingComponentFeature
from panel_machining_feature import PanelMachiningFeature
from cabinet_feature_manifest import CabinetFeatureManifest
from cabinet_lighting_file_set_renderer import CabinetLightingFileSetRenderer
from lighting_generated_file_record import LightingGeneratedFileRecord
from lighting_run import LightingRun
from part_lighting_plan import PartLightingPlan


@dataclass(frozen=True, slots=True)
class CabinetLightingGenerationResult:
    """Report the saved plan and changed project files."""

    plan: PartLightingPlan
    written_paths: tuple[Path, ...]


class CabinetLightingGenerator:
    """Attach one part-owned light without rewriting cabinet taxonomy."""

    _MODULE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

    def __init__(self) -> None:
        self.assembly_loader = GeneratedAssemblyBuilderLoader()
        self.renderer = CabinetLightingFileSetRenderer()
        self.writer = AssemblyTaxonomyWriter()
        self.features = CabinetFeatureManifest()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        part_id: str,
        run: LightingRun,
        *,
        base_builder_module: str,
    ) -> CabinetLightingGenerationResult:
        if not self._MODULE_PATTERN.fullmatch(base_builder_module):
            raise ValueError("base builder module must be a stable Python name")
        if base_builder_module not in {"builder", "complete_builder"}:
            raise ValueError("Move existing features into complete_builder before adding lighting")
        built = self.assembly_loader.load_assembly(project_root, assembly_id, exclude_features=("lighting.feature",))
        assembly = built.spec
        part = assembly.part(part_id)
        if not part.inside_face:
            raise ValueError(f"{part_id} does not declare an inside face")
        plan = PartLightingPlan(assembly_id, part_id, part.inside_face, run)
        LightingComponentFeature(plan).validate_owner(assembly)
        request = LightingMachiningRecipe().build(part, plan)
        PanelMachiningFeature().apply(built, (request,))
        files = self.renderer.render(plan, base_builder_module)
        recorded = LightingGeneratedFileRecord.load(project_root, assembly_id)
        written = self.writer.write(project_root, files, recorded=recorded)
        LightingGeneratedFileRecord.from_rendered(assembly_id, files).save(project_root)
        manifest = self.features.register(
            project_root,
            assembly_id,
            "lighting.feature",
            30,
            affected_manufactured_part_paths=(part_id,),
            affected_purchased_hardware_paths=(run.run_id,),
        )
        return CabinetLightingGenerationResult(
            plan,
            written
            + ((manifest.relative_to(project_root),) if manifest else ()),
        )


__all__ = ["CabinetLightingGenerationResult", "CabinetLightingGenerator"]
