"""Scope: Translate one sourced MOVENTO runner into drawer-box sizing values."""

from __future__ import annotations

from drawer_box_spec import DrawerBoxSizingProfile
from movento_runner_profile import MoventoRunnerProfile


class MoventoDrawerBoxProfileAdapter:
    """Keep hardware-owned deductions authoritative in drawer-box planning."""

    def build(
        self,
        runner: MoventoRunnerProfile,
        *,
        side_thickness_mm: float,
        front_back_thickness_mm: float,
        bottom_thickness_mm: float,
        bottom_underside_recess_mm: float,
        box_height_mm: float,
    ) -> DrawerBoxSizingProfile:
        if side_thickness_mm > runner.maximum_drawer_side_thickness_mm:
            raise ValueError(
                f"drawer sides exceed {runner.maximum_drawer_side_thickness_mm:g} mm"
            )
        recess_limits = (
            runner.drawer_bottom_recess_minimum_mm,
            runner.drawer_bottom_recess_maximum_mm,
        )
        if not recess_limits[0] <= bottom_underside_recess_mm <= recess_limits[1]:
            raise ValueError(
                "drawer bottom recess falls outside the selected runner limits"
            )
        return DrawerBoxSizingProfile(
            runner_length_mm=runner.nominal_length_mm,
            drawer_inside_width_reduction_mm=(
                runner.drawer_inside_width_deduction_mm
            ),
            runner_to_side_length_reduction_mm=(
                runner.drawer_side_length_deduction_mm
            ),
            side_thickness_mm=side_thickness_mm,
            front_back_thickness_mm=front_back_thickness_mm,
            bottom_thickness_mm=bottom_thickness_mm,
            bottom_underside_recess_mm=bottom_underside_recess_mm,
            box_height_mm=box_height_mm,
        )


__all__ = ["MoventoDrawerBoxProfileAdapter"]
