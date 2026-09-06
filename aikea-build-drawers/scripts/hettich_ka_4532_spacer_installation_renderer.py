"""Scope: Render one drawer and four exact purchased hardware instances."""

from __future__ import annotations

from hettich_ka_4532_spacer_hardware_spec_renderer import (
    HettichKa4532SpacerHardwareSpecRenderer,
)


class HettichKa4532SpacerInstallationRenderer:
    """Persist separate articulated runner frames and both spacer instances."""

    def __init__(self) -> None:
        self.hardware = HettichKa4532SpacerHardwareSpecRenderer()

    def render(self, plan) -> str:
        mounting = plan.hardware_mounting
        x_mm, y_mm, z_mm = plan.origin_in_parent_mm
        return (
            f'"""Scope: Place {plan.drawer.assembly_id} and its exact Hettich set."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, ChildAssemblySpec, LocalToParentPlacement,\n"
            "    Point3D, PurchasedHardwareSpec,\n"
            ")\n"
            "from hettich_ka_4532_spacer_mounting_plan import (\n"
            "    HettichKa4532SpacerMountingPlan,\n"
            ")\n"
            "from drawer_hardware_mounting_plan import HardwarePlacement\n\n\n"
            "DRAWER_CHILD = ChildAssemblySpec(\n"
            f"    assembly_id={plan.drawer.assembly_id!r}, purpose='drawer',\n"
            "    local_to_parent=LocalToParentPlacement(\n"
            f"        origin_in_parent=Point3D({x_mm!r}, {y_mm!r}, {z_mm!r}),\n"
            "        axis_basis=AxisBasis(\n"
            "            AxisDirection(1.0, 0.0, 0.0),\n"
            "            AxisDirection(0.0, 1.0, 0.0),\n"
            "            AxisDirection(0.0, 0.0, 1.0),\n"
            "        ),\n"
            "    ),\n"
            ")\n"
            "CHILD_ASSEMBLIES = (DRAWER_CHILD,)\n\n"
            + self._mounting_plan_source(plan)
            + "\n"
            + self.hardware.render(plan)
        )

    def _mounting_plan_source(self, plan) -> str:
        mounting = plan.hardware_mounting
        fields = (
            "spacer_left_in_cabinet",
            "spacer_right_in_cabinet",
            "fixed_runner_left_in_cabinet",
            "fixed_runner_right_in_cabinet",
            "moving_runner_left_in_drawer",
            "moving_runner_right_in_drawer",
        )
        placements = "".join(
            f"    {name}="
            + self._plan_placement(getattr(mounting, name))
            + ",\n"
            for name in fields
        )
        return (
            "MOUNTING_PLAN = HettichKa4532SpacerMountingPlan(\n"
            f"    cabinet_front_mm={mounting.cabinet_front_mm!r},\n"
            f"    drawer_front_mm={mounting.drawer_front_mm!r},\n"
            f"    drawer_origin_mm={mounting.drawer_origin_mm!r},\n"
            f"    drawer_outside_width_mm={mounting.drawer_outside_width_mm!r},\n"
            f"{placements}"
            ")\n"
        )

    def _plan_placement(self, placement) -> str:
        return (
            "HardwarePlacement("
            f"{placement.origin_mm!r}, "
            f"{placement.local_x_in_owner!r}, "
            f"{placement.local_y_in_owner!r}, "
            f"{placement.local_z_in_owner!r}"
            ")"
        )

__all__ = ["HettichKa4532SpacerInstallationRenderer"]
