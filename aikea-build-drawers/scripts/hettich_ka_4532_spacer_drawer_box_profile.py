"""Scope: Translate the KA 4532 spacer set into generic drawer-box sizing."""

from __future__ import annotations

from drawer_box_spec import DrawerBoxSizingProfile
from hettich_ka_4532_spacer_profile import HettichKa4532SpacerProfile


class HettichKa4532SpacerDrawerBoxProfileAdapter:
    """Size a five-sheet drawer between two spacer-mounted runner sides."""

    def build(
        self,
        hardware: HettichKa4532SpacerProfile,
        *,
        side_thickness_mm: float,
        front_back_thickness_mm: float,
        bottom_thickness_mm: float,
        bottom_underside_recess_mm: float,
        box_height_mm: float,
    ) -> DrawerBoxSizingProfile:
        return DrawerBoxSizingProfile(
            runner_length_mm=hardware.nominal_runner_length_mm,
            drawer_inside_width_reduction_mm=(
                2.0 * (hardware.hardware_width_per_side_mm + side_thickness_mm)
            ),
            runner_to_side_length_reduction_mm=0.0,
            side_thickness_mm=side_thickness_mm,
            front_back_thickness_mm=front_back_thickness_mm,
            bottom_thickness_mm=bottom_thickness_mm,
            bottom_underside_recess_mm=bottom_underside_recess_mm,
            box_height_mm=box_height_mm,
        )


__all__ = ["HettichKa4532SpacerDrawerBoxProfileAdapter"]
