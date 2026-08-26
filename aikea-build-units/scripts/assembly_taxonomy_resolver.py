"""Scope: Resolve global project inputs into complete local assembly taxonomies."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from assembly_run import AssemblyRun, AssemblyRunItem, AssemblyRunReader
from assembly_taxonomy import (
    AssemblyTaxonomyInputError,
    BoundaryPoint,
    LocalAssemblyTaxonomy,
    ProjectAssemblyTaxonomy,
)
from assembly_taxonomy_profiles import AssemblyTaxonomyProfileRegistry
from overall_wardrobe_calculator import OverallWardrobeCalculator
from overall_wardrobe_inputs import OverallWardrobeInputs, OverallWardrobeInputReader
from overall_wardrobe_results import CabinetOverallSize
from top_boundary import TopBoundaryKind


class AssemblyTaxonomyResolver:
    """Calculate every inherited local value before files are written."""

    def __init__(self) -> None:
        self.profiles = AssemblyTaxonomyProfileRegistry()

    def resolve(self, project: dict[str, Any]) -> ProjectAssemblyTaxonomy:
        run = AssemblyRunReader().read(project)
        inputs = OverallWardrobeInputReader().read(self._overall_project(project, run))
        result = OverallWardrobeCalculator().calculate(inputs)
        assemblies = tuple(
            self._resolve_assembly(item, size, inputs, result.inside_depth_mm)
            for item, size in zip(run.assemblies, result.cabinets)
        )
        return ProjectAssemblyTaxonomy(assemblies)

    def _overall_project(
        self, project: dict[str, Any], run: AssemblyRun
    ) -> dict[str, Any]:
        adapted = deepcopy(project)
        settings = adapted["design_settings"]
        settings.pop("assembly_run")
        settings["cabinet_run"] = {
            "cabinet_count": len(run.assemblies),
            "cabinet_width_shares": [item.width_share for item in run.assemblies],
            "left_clearance": run.left_clearance,
            "right_clearance": run.right_clearance,
            "cabinet_gap": run.gap,
            "ceiling_clearance": run.ceiling_clearance,
        }
        return adapted

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
        allowances = settings.fitted_dimensions.resolve_fitting_allowances(
            settings.fit_allowance_mm
        )
        depth_mm = (
            inputs.space.minimum_depth_mm
            - allowances.depth_mm
            - settings.door_thickness_mm
        )
        parts = profile.build_parts(
            top,
            size.width_mm,
            depth_mm,
            size.door_width_mm,
            settings.base_height_mm,
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
            parts,
            profile.build_joints(len(top) - 1),
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
