"""Scope: Export one generated cabinet with its saved recessed light."""

from __future__ import annotations

from pathlib import Path

from cabinet_lighting_placement import CabinetLightingPlacementBuilder
from cabinet_lighting_review import CabinetLightingReviewResult
from cabinet_review_geometry import CabinetReviewGeometry
from cadquery_glb_exporter import CadQueryGlbExporter
from door_review_state import DoorReviewState
from generated_assembly_builder_loader import GeneratedAssemblyBuilderLoader
from hettich_ka_5332_drawers_review_geometry import HettichKa5332DrawersReviewGeometry
from hettich_ka_5332_saved_drawers_loader import HettichKa5332SavedDrawersLoader
from hettich_ka_5332_step_assembly import HettichKa5332StepAssemblyLoader
from part_lighting_builder import PartLightingBuilder
from part_lighting_fit_checker import PartLightingFitChecker
from part_lighting_plan_loader import PartLightingPlanLoader
from unit_mockup import MockupPart, UnitMockupInputError


class CabinetLightingReviewGenerator:
    """Rebuild, fit-check, and export one cabinet from its generated files."""

    _LIGHTING_BUILDER_MODULE = "with_lighting_builder"

    def __init__(self) -> None:
        self.assembly_loader = GeneratedAssemblyBuilderLoader()
        self.plan_loader = PartLightingPlanLoader()
        self.part_lighting = PartLightingBuilder()
        self.placement = CabinetLightingPlacementBuilder()
        self.fit_checker = PartLightingFitChecker()
        self.cabinet_geometry = CabinetReviewGeometry()
        self.saved_drawers = HettichKa5332SavedDrawersLoader()
        self.drawer_geometry = HettichKa5332DrawersReviewGeometry()
        self.step_loader = HettichKa5332StepAssemblyLoader()
        self.exporter = CadQueryGlbExporter()

    def generate(
        self,
        project_root: Path,
        assembly_id: str,
        part_id: str,
        *,
        base_builder_module: str,
        hardware_directory: Path,
        door_state: DoorReviewState = DoorReviewState.REMOVED,
    ) -> CabinetLightingReviewResult:
        base = self.assembly_loader.load_assembly(
            project_root,
            assembly_id,
            base_builder_module,
        )
        lit = self.assembly_loader.load_assembly(
            project_root,
            assembly_id,
            self._LIGHTING_BUILDER_MODULE,
        )
        plan_path = project_root / "assemblies" / assembly_id / "parts" / part_id / "lighting.yaml"
        plan = self.plan_loader.load(plan_path)
        original_host = next(part for part in base.parts if part.spec.part_id == part_id)
        lighting = self.part_lighting.build(original_host, plan)
        host_in_lit = next(part for part in lit.parts if part.spec.part_id == part_id)
        if abs(host_in_lit.solid.val().Volume() - lighting.part.solid.val().Volume()) > 0.01:
            raise UnitMockupInputError(["generated cabinet does not contain its saved groove"])
        cabinet_parts = self.cabinet_geometry.build(lit, door_state)
        drawers, hardware = self._drawer_parts(project_root, assembly_id, lit, hardware_directory)
        placement = self.placement.build(lit.spec, original_host.spec, plan)
        other_parts = tuple(part for part in cabinet_parts if part.name != part_id) + drawers + hardware
        report = self.fit_checker.check(
            lit.spec,
            original_host,
            lighting,
            plan,
            placement,
            other_parts,
        )
        if not report.is_valid:
            raise UnitMockupInputError(["cabinet lighting fit check failed"])
        fit_report_path = project_root / "assemblies" / assembly_id / "lighting-fit-check.json"
        report.write(fit_report_path)
        review_parts = cabinet_parts + drawers + hardware + self._light_parts(lighting, plan, placement)
        glb_path = project_root / "assemblies" / assembly_id / f"{assembly_id}_lighting_review.glb"
        self.exporter.export(f"{assembly_id}_lighting_review", review_parts, glb_path)
        return CabinetLightingReviewResult(assembly_id, glb_path, fit_report_path)

    def _drawer_parts(self, project_root, assembly_id, cabinet, hardware_directory):
        saved = self.saved_drawers.load(project_root, assembly_id, cabinet)
        step = self.step_loader.load(hardware_directory)
        steps = {str(saved_item.runner_item_number): step for saved_item in saved}
        return (
            self.drawer_geometry.build_drawers(saved, {}),
            self.drawer_geometry.build_hardware(saved, steps, {}),
        )

    def _light_parts(self, lighting, plan, placement):
        profile_id = plan.run.profile.profile_id
        return (
            MockupPart(
                f"purchased_light__{profile_id}__body",
                lighting.luminaire_body,
                placement.luminaire_location,
                (0.23, 0.24, 0.22, 1.0),
            ),
            MockupPart(
                f"light_source__{profile_id}__{plan.run.color_temperature_k}k",
                lighting.emitter_face,
                placement.luminaire_location,
                (1.0, 0.76, 0.50, 1.0),
            ),
        )


__all__ = ["CabinetLightingReviewGenerator"]
