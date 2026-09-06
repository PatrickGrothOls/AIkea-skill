"""Scope: Resolve global project inputs into complete local assembly taxonomies."""

from __future__ import annotations

from typing import Any

from assembly_run import AssemblyRunItem, AssemblyRunReader
from assembly_run_overall_project_adapter import AssemblyRunOverallProjectAdapter
from assembly_taxonomy import (
    AssemblyTaxonomyInputError,
    BoundaryPoint,
    LocalAssemblyTaxonomy,
    ProjectAssemblyTaxonomy,
)
from assembly_taxonomy_profiles import AssemblyTaxonomyProfileRegistry
from base_taxonomy_builder import BaseTaxonomyBuilder
from door_bottom_height_resolver import DoorBottomHeightResolver
from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputs, OverallWardrobeInputReader
from overall_wardrobe_results import CabinetOverallSize
from project_part_placement_resolver import ProjectPartPlacementResolver
from top_boundary import TopBoundaryKind
from wardrobe_taxonomy_resolver import WardrobeTaxonomyResolver


class AssemblyTaxonomyResolver:
    """Calculate every inherited local value before files are written."""

    def __init__(self) -> None:
        self.profiles = AssemblyTaxonomyProfileRegistry()
        self.base_taxonomy = BaseTaxonomyBuilder()
        self.overall_project = AssemblyRunOverallProjectAdapter()
        self.door_bottom_height = DoorBottomHeightResolver()
        self.part_placements = ProjectPartPlacementResolver()
        self.wardrobe = WardrobeTaxonomyResolver()

    def resolve(self, project: dict[str, Any]) -> ProjectAssemblyTaxonomy:
        run = AssemblyRunReader().read(project)
        inputs = OverallWardrobeInputReader().read(self.overall_project.adapt(project, run))
        result = OverallWardrobeCalculator().calculate(inputs)
        cabinets = tuple(
            self._resolve_assembly(item, size, inputs, result.inside_depth_mm)
            for item, size in zip(run.assemblies, result.cabinets)
        )
        base = self.base_taxonomy.build(
            tuple(
                (size.left_position_mm, size.right_position_mm)
                for size in result.cabinets
            ),
            self._depth_mm(inputs),
            inputs.settings.base_height_mm,
            inputs.settings.cabinet_panel_thickness_mm,
            inputs.settings.plinth_front.value,
            inputs.settings.plinth_recess_mm,
        )
        placed = self.part_placements.resolve(
            ProjectAssemblyTaxonomy((*cabinets, base))
        )
        return self.wardrobe.resolve(placed)

    def _resolve_assembly(
        self,
        item: AssemblyRunItem,
        size: CabinetOverallSize,
        inputs: OverallWardrobeInputs,
        inside_depth_mm: float,
    ) -> LocalAssemblyTaxonomy:
        profile = self.profiles.get(item.purpose)
        if profile is None:
            raise AssemblyTaxonomyInputError(
                [f"no local construction taxonomy exists for purpose '{item.purpose}'"]
            )
        top = self._local_top(size, inputs)
        settings = inputs.settings
        depth_mm = self._depth_mm(inputs)
        door_bottom_mm = self.door_bottom_height.resolve(
            settings.door_bottom,
            settings.base_height_mm,
            settings.cabinet_panel_thickness_mm,
        )
        parts = profile.build_parts(
            top,
            size.width_mm,
            inside_depth_mm,
            size.door_width_mm,
            settings.base_height_mm,
            door_bottom_mm,
            settings.cabinet_panel_thickness_mm,
            settings.door_thickness_mm,
            settings.back_panel_thickness_mm,
        )
        return LocalAssemblyTaxonomy(
            item.assembly_id,
            item.purpose,
            size.left_position_mm,
            size.right_position_mm,
            size.width_mm,
            top,
            depth_mm,
            inside_depth_mm,
            size.door_width_mm,
            settings.base_height_mm,
            settings.door_bottom.value,
            door_bottom_mm,
            parts,
            profile.build_joints(top),
        )

    def _depth_mm(self, inputs: OverallWardrobeInputs) -> float:
        settings = inputs.settings
        allowances = settings.fitted_dimensions.resolve_fitting_allowances(
            settings.fit_allowance_mm
        )
        return (
            inputs.space.minimum_depth_mm
            - allowances.depth_mm
            - settings.door_thickness_mm
        )

    def _local_top(
        self, size: CabinetOverallSize, inputs: OverallWardrobeInputs
    ) -> tuple[BoundaryPoint, ...]:
        boundary = inputs.space.top_boundary
        positions = [size.left_position_mm]
        if boundary.kind is TopBoundaryKind.MEASURED_PROFILE:
            positions.extend(
                item.distance_from_left_mm
                for item in boundary.measurements
                if size.left_position_mm < item.distance_from_left_mm < size.right_position_mm
            )
        positions.append(size.right_position_mm)
        allowance = inputs.settings.fitted_dimensions.resolve_fitting_allowances(
            inputs.settings.fit_allowance_mm
        ).height_mm
        return tuple(
            BoundaryPoint(
                position - size.left_position_mm,
                boundary.height_at(position)
                - allowance
                - inputs.settings.base_height_mm
                - inputs.settings.ceiling_clearance_mm,
            )
            for position in positions
        )
