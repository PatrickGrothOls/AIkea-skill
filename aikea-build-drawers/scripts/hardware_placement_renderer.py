"""Scope: Render one calculated hardware frame as generated Python source."""

from __future__ import annotations

from drawer_hardware_mounting_plan import HardwarePlacement


class HardwarePlacementRenderer:
    """Write a placement without changing its origin or manufacturer axes."""

    def render(self, placement: HardwarePlacement, indentation: str) -> str:
        origin = placement.origin_mm
        x_axis = placement.local_x_in_owner
        y_axis = placement.local_y_in_owner
        z_axis = placement.local_z_in_owner
        nested = indentation + "    "
        return (
            "LocalToParentPlacement(\n"
            f"{nested}origin_in_parent=Point3D{origin!r},\n"
            f"{nested}axis_basis=AxisBasis(\n"
            f"{nested}    AxisDirection{x_axis!r},\n"
            f"{nested}    AxisDirection{y_axis!r},\n"
            f"{nested}    AxisDirection{z_axis!r},\n"
            f"{nested}),\n"
            f"{indentation})"
        )


__all__ = ["HardwarePlacementRenderer"]
