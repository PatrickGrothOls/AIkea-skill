"""Scope: Render one placed drawer-box specification as Python source."""

from __future__ import annotations

from drawer_box_spec import DrawerBoxSpec, DrawerPartSpec
from drawer_part_locator import DrawerPartPlacement


class DrawerBoxSpecSourceRenderer:
    """Preserve every planned drawer dimension and part-local frame."""

    def render(self, box: DrawerBoxSpec) -> str:
        opening = box.opening
        sizing = box.sizing
        parts = "\n".join(self._part(part) for part in box.parts)
        return (
            "DrawerBoxSpec(\n"
            "    opening=CabinetDrawerOpening(\n"
            f"        clear_width_mm={opening.clear_width_mm!r},\n"
            f"        inside_depth_mm={opening.inside_depth_mm!r},\n"
            "    ),\n"
            "    sizing=DrawerBoxSizingProfile(\n"
            f"        runner_length_mm={sizing.runner_length_mm!r},\n"
            f"        drawer_inside_width_reduction_mm={sizing.drawer_inside_width_reduction_mm!r},\n"
            f"        runner_to_side_length_reduction_mm={sizing.runner_to_side_length_reduction_mm!r},\n"
            f"        side_thickness_mm={sizing.side_thickness_mm!r},\n"
            f"        front_back_thickness_mm={sizing.front_back_thickness_mm!r},\n"
            f"        bottom_thickness_mm={sizing.bottom_thickness_mm!r},\n"
            f"        bottom_underside_recess_mm={sizing.bottom_underside_recess_mm!r},\n"
            f"        box_height_mm={sizing.box_height_mm!r},\n"
            "    ),\n"
            f"    clear_inside_width_mm={box.clear_inside_width_mm!r},\n"
            f"    outside_width_mm={box.outside_width_mm!r},\n"
            f"    side_length_mm={box.side_length_mm!r},\n"
            f"    outside_depth_mm={box.outside_depth_mm!r},\n"
            f"    clear_inside_depth_mm={box.clear_inside_depth_mm!r},\n"
            "    parts=(\n"
            f"{parts}\n"
            "    ),\n"
            ")"
        )

    def _part(self, part: DrawerPartSpec) -> str:
        placement = part.local_to_parent
        if placement is None:
            raise ValueError(f"drawer part has no placement: {part.part_id}")
        return (
            "        DrawerPartSpec(\n"
            f"            part_id={part.part_id!r},\n"
            f"            role={part.role!r},\n"
            f"            width_mm={part.width_mm!r},\n"
            f"            height_mm={part.height_mm!r},\n"
            f"            thickness_mm={part.thickness_mm!r},\n"
            f"            local_to_parent={self._placement(placement)},\n"
            "        ),"
        )

    def _placement(self, placement: DrawerPartPlacement) -> str:
        origin = placement.origin_in_parent
        axes = placement.axis_basis
        return (
            "LocalToParentPlacement("
            f"Point3D({origin.x_mm!r}, {origin.y_mm!r}, {origin.z_mm!r}), "
            "AxisBasis("
            f"{self._axis(axes.local_x_in_parent)}, "
            f"{self._axis(axes.local_y_in_parent)}, "
            f"{self._axis(axes.local_z_in_parent)}"
            ")"
            ")"
        )

    def _axis(self, direction) -> str:
        return f"AxisDirection({direction.x!r}, {direction.y!r}, {direction.z!r})"


__all__ = ["DrawerBoxSpecSourceRenderer"]
