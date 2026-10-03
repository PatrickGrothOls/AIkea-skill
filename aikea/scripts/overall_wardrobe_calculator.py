"""Scope: Calculate safe overall cabinet dimensions from checked project inputs."""

from __future__ import annotations

from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputs
from overall_wardrobe_results import CabinetOverallSize, OverallWardrobeResult


class OverallWardrobeCalculator:
    """Apply dimension-specific fitting room and distribute the cabinet run."""

    def calculate(self, inputs: OverallWardrobeInputs) -> OverallWardrobeResult:
        space = inputs.space
        settings = inputs.settings
        allowances = settings.fitted_dimensions.resolve_fitting_allowances(
            settings.fit_allowance_mm
        )
        usable_width = space.minimum_width_mm - allowances.width_mm
        usable_depth = space.minimum_depth_mm - allowances.depth_mm
        problems = self._find_impossible_dimensions(
            inputs,
            usable_width,
            usable_depth,
            allowances.height_mm,
        )
        if problems:
            raise OverallWardrobeInputError(problems)
        total_gaps = settings.cabinet_gap_mm * (settings.cabinet_count - 1)
        distributable_width = (
            usable_width
            - settings.left_clearance_mm
            - settings.right_clearance_mm
            - total_gaps
        )
        width_per_share = distributable_width / sum(settings.cabinet_width_shares)
        cabinet_depth = usable_depth - settings.door_thickness_mm
        inside_depth = cabinet_depth - settings.back_panel_thickness_mm
        cabinets = self._build_cabinet_sizes(
            inputs,
            width_per_share,
            allowances.height_mm,
        )
        return OverallWardrobeResult(
            minimum_measured_width_mm=space.minimum_width_mm,
            minimum_measured_depth_mm=space.minimum_depth_mm,
            width_fitting_allowance_mm=allowances.width_mm,
            depth_fitting_allowance_mm=allowances.depth_mm,
            height_fitting_allowance_mm=allowances.height_mm,
            usable_width_mm=usable_width,
            usable_depth_mm=usable_depth,
            cabinet_depth_mm=cabinet_depth,
            inside_depth_mm=inside_depth,
            cabinets=cabinets,
        )

    def _build_cabinet_sizes(
        self,
        inputs: OverallWardrobeInputs,
        width_per_share: float,
        height_fitting_allowance_mm: float,
    ) -> tuple[CabinetOverallSize, ...]:
        settings = inputs.settings
        cabinets: list[CabinetOverallSize] = []
        left_position = settings.left_clearance_mm
        for index, share in enumerate(settings.cabinet_width_shares):
            width = width_per_share * share
            right_position = left_position + width
            cabinets.append(
                CabinetOverallSize(
                    cabinet_number=index + 1,
                    left_position_mm=left_position,
                    right_position_mm=right_position,
                    width_mm=width,
                    left_height_mm=self._cabinet_height_at(
                        inputs,
                        left_position,
                        height_fitting_allowance_mm,
                    ),
                    right_height_mm=self._cabinet_height_at(
                        inputs,
                        right_position,
                        height_fitting_allowance_mm,
                    ),
                    door_width_mm=width - settings.door_gap_mm,
                )
            )
            left_position = right_position + settings.cabinet_gap_mm
        return tuple(cabinets)

    def _find_impossible_dimensions(
        self,
        inputs: OverallWardrobeInputs,
        usable_width: float,
        usable_depth: float,
        height_fitting_allowance_mm: float,
    ) -> list[str]:
        settings = inputs.settings
        problems: list[str] = []
        used_width = (
            settings.left_clearance_mm
            + settings.right_clearance_mm
            + settings.cabinet_gap_mm * (settings.cabinet_count - 1)
        )
        if usable_width <= 0:
            problems.append("fit allowance leaves no usable width")
        elif used_width >= usable_width:
            problems.append("clearances and cabinet gaps leave no width for cabinets")
        if usable_depth <= 0:
            problems.append("fit allowance leaves no usable depth")
        elif settings.door_thickness_mm + settings.back_panel_thickness_mm >= usable_depth:
            problems.append("door and back thicknesses leave no positive inside depth")
        if usable_width > used_width:
            available_width = usable_width - used_width
            narrowest_width = (
                available_width
                * min(settings.cabinet_width_shares)
                / sum(settings.cabinet_width_shares)
            )
            if settings.door_gap_mm >= narrowest_width:
                problems.append("door gap must be smaller than every cabinet width")
        minimum_height = inputs.space.minimum_height_mm
        used_height = (
            height_fitting_allowance_mm
            + settings.base_height_mm
            + settings.ceiling_clearance_mm
        )
        if used_height >= minimum_height:
            problems.append("fit allowance, base, and ceiling clearance leave no cabinet height")
        return problems

    def _cabinet_height_at(
        self,
        inputs: OverallWardrobeInputs,
        position_mm: float,
        height_fitting_allowance_mm: float,
    ) -> float:
        settings = inputs.settings
        measured_height = inputs.space.top_boundary.height_at(position_mm)
        return (
            measured_height
            - height_fitting_allowance_mm
            - settings.base_height_mm
            - settings.ceiling_clearance_mm
        )
