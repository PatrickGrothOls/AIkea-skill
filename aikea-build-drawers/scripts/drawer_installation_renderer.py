"""Scope: Render drawer-child and fixed-runner installation specifications."""

from __future__ import annotations

from cabinet_drawer_plan import CabinetDrawerPlan
from hardware_placement_renderer import HardwarePlacementRenderer


class DrawerInstallationRenderer:
    """Write the cabinet-owned child and runner frames as Python source."""

    def __init__(self) -> None:
        self.placement_renderer = HardwarePlacementRenderer()

    def render(self, plan: CabinetDrawerPlan) -> str:
        hardware = plan.runner.require_hardware_asset_set()
        mounting = plan.hardware_mounting
        x_mm, y_mm, z_mm = plan.origin_in_parent_mm
        return (
            f'"""Scope: Place drawer children owned by {plan.parent_assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, ChildAssemblySpec, LocalToParentPlacement, Point3D,\n"
            "    PurchasedHardwareSpec,\n"
            ")\n\n\n"
            "DRAWER_CHILD = ChildAssemblySpec(\n"
            f"    assembly_id={plan.drawer.assembly_id!r},\n"
            "    purpose='drawer',\n"
            "    local_to_parent=LocalToParentPlacement(\n"
            f"        origin_in_parent=Point3D({x_mm!r}, {y_mm!r}, {z_mm!r}),\n"
            "        axis_basis=AxisBasis(\n"
            "            AxisDirection(1.0, 0.0, 0.0),\n"
            "            AxisDirection(0.0, 1.0, 0.0),\n"
            "            AxisDirection(0.0, 0.0, 1.0),\n"
            "        ),\n"
            "    ),\n"
            ")\n"
            "CHILD_ASSEMBLIES = (DRAWER_CHILD,)\n"
            "FIXED_RUNNERS = (\n"
            + self._hardware_source(
                "runner_left",
                hardware.runner_left.product_code,
                hardware.runner_left.asset_id,
                mounting.runner_left_in_cabinet,
            )
            + self._hardware_source(
                "runner_right",
                hardware.runner_right.product_code,
                hardware.runner_right.asset_id,
                mounting.runner_right_in_cabinet,
            )
            + ")\n"
        )

    def _hardware_source(
        self,
        hardware_id: str,
        product_code: str,
        asset_id: str,
        placement,
    ) -> str:
        return (
            "    PurchasedHardwareSpec(\n"
            f"        {hardware_id!r}, 'Blum', {product_code!r},\n"
            f"        {asset_id!r},\n"
            "        local_to_parent="
            + self.placement_renderer.render(placement, "        ")
            + ",\n"
            "    ),\n"
        )


__all__ = ["DrawerInstallationRenderer"]
