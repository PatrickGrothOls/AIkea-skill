"""Scope: Calculate one wooden drawer box from its cabinet opening and sizing profile."""

from __future__ import annotations

from dataclasses import replace

from drawer_box_spec import (
    CabinetDrawerOpening,
    DrawerBoxSizingProfile,
    DrawerBoxSpec,
    DrawerPartSpec,
)
from drawer_part_locator import DrawerPartLocator


class DrawerBoxPlanningError(ValueError):
    """Report sizing values that cannot produce a physical drawer box."""


class DrawerBoxPlanner:
    """Resolve five rectangular sheet parts without adding joinery machining."""

    def __init__(self) -> None:
        self.part_placements = DrawerPartLocator()

    def plan(
        self,
        opening: CabinetDrawerOpening,
        sizing: DrawerBoxSizingProfile,
    ) -> DrawerBoxSpec:
        self._require_positive_values(opening, sizing)
        clear_width_mm = (
            opening.clear_width_mm - sizing.drawer_inside_width_reduction_mm
        )
        outside_width_mm = clear_width_mm + (2.0 * sizing.side_thickness_mm)
        side_length_mm = (
            sizing.runner_length_mm - sizing.runner_to_side_length_reduction_mm
        )
        clear_depth_mm = side_length_mm
        outside_depth_mm = side_length_mm + (
            2.0 * sizing.front_back_thickness_mm
        )
        if min(clear_width_mm, clear_depth_mm) <= 0.0:
            raise DrawerBoxPlanningError(
                "the opening and sizing profile leave no drawer interior"
            )
        if outside_depth_mm > opening.inside_depth_mm:
            raise DrawerBoxPlanningError(
                "the complete drawer is deeper than the cabinet opening"
            )
        if (
            sizing.bottom_underside_recess_mm + sizing.bottom_thickness_mm
            >= sizing.box_height_mm
        ):
            raise DrawerBoxPlanningError(
                "the drawer bottom must remain below the top of the box"
            )

        parts = (
            self._part("left_side", "drawer_side", side_length_mm, sizing),
            self._part("right_side", "drawer_side", side_length_mm, sizing),
            self._part("front", "drawer_front", outside_width_mm, sizing),
            self._part("back", "drawer_back", outside_width_mm, sizing),
            DrawerPartSpec(
                part_id="bottom",
                role="drawer_bottom",
                width_mm=clear_width_mm,
                height_mm=clear_depth_mm,
                thickness_mm=sizing.bottom_thickness_mm,
            ),
        )
        box = DrawerBoxSpec(
            opening=opening,
            sizing=sizing,
            clear_inside_width_mm=clear_width_mm,
            outside_width_mm=outside_width_mm,
            side_length_mm=side_length_mm,
            outside_depth_mm=outside_depth_mm,
            clear_inside_depth_mm=clear_depth_mm,
            parts=parts,
        )
        placed_parts = tuple(
            replace(
                part,
                local_to_parent=self.part_placements.placement(part.part_id, box),
            )
            for part in box.parts
        )
        return replace(box, parts=placed_parts)

    def _part(
        self,
        part_id: str,
        role: str,
        width_mm: float,
        sizing: DrawerBoxSizingProfile,
    ) -> DrawerPartSpec:
        thickness_mm = (
            sizing.side_thickness_mm
            if role == "drawer_side"
            else sizing.front_back_thickness_mm
        )
        return DrawerPartSpec(
            part_id=part_id,
            role=role,
            width_mm=width_mm,
            height_mm=sizing.box_height_mm,
            thickness_mm=thickness_mm,
        )

    def _require_positive_values(
        self,
        opening: CabinetDrawerOpening,
        sizing: DrawerBoxSizingProfile,
    ) -> None:
        values = {
            "opening clear width": opening.clear_width_mm,
            "opening inside depth": opening.inside_depth_mm,
            "runner length": sizing.runner_length_mm,
            "side thickness": sizing.side_thickness_mm,
            "front and back thickness": sizing.front_back_thickness_mm,
            "bottom thickness": sizing.bottom_thickness_mm,
            "box height": sizing.box_height_mm,
        }
        invalid = [name for name, value in values.items() if value <= 0.0]
        if invalid:
            raise DrawerBoxPlanningError(
                f"drawer sizing values must be positive: {', '.join(invalid)}"
            )


__all__ = ["DrawerBoxPlanner", "DrawerBoxPlanningError"]
