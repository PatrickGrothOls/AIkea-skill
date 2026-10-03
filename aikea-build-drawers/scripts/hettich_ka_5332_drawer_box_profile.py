"""Scope: Translate KA 5332 side clearance into generic drawer-box sizing."""

from __future__ import annotations

from drawer_box_spec import DrawerBoxSizingProfile
from hettich_ka_5332_runner_profile import HettichKa5332RunnerProfile


class HettichKa5332DrawerBoxProfileAdapter:
    """Make a five-sheet drawer fit between the two side-mounted runners."""

    def build(
        self,
        runner: HettichKa5332RunnerProfile,
        *,
        side_thickness_mm: float,
        front_back_thickness_mm: float,
        bottom_thickness_mm: float,
        bottom_underside_recess_mm: float,
        box_height_mm: float,
    ) -> DrawerBoxSizingProfile:
        return DrawerBoxSizingProfile(
            runner_length_mm=runner.nominal_length_mm,
            drawer_inside_width_reduction_mm=(
                2.0 * (runner.installed_width_per_side_mm + side_thickness_mm)
            ),
            runner_to_side_length_reduction_mm=0.0,
            side_thickness_mm=side_thickness_mm,
            front_back_thickness_mm=front_back_thickness_mm,
            bottom_thickness_mm=bottom_thickness_mm,
            bottom_underside_recess_mm=bottom_underside_recess_mm,
            box_height_mm=box_height_mm,
        )


__all__ = ["HettichKa5332DrawerBoxProfileAdapter"]
