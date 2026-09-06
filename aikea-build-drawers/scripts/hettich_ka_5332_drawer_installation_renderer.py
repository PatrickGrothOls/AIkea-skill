"""Scope: Render one KA 5332 child frame and paired-runner installation."""

from __future__ import annotations

from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
)


class HettichKa5332DrawerInstallationRenderer:
    """Save one purchased pair plus exact placements for its two source sides."""

    def render(self, plan: HettichKa5332CabinetDrawerPlan) -> str:
        mounting = plan.hardware_mounting
        x_mm, y_mm, z_mm = plan.origin_in_parent_mm
        return (
            f'"""Scope: Place drawer and KA 5332 hardware owned by {plan.parent_assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, ChildAssemblySpec, LocalToParentPlacement, Point3D,\n"
            "    PurchasedHardwareSpec,\n"
            ")\n\n\n"
            "SOURCE_MEMBERS_PER_SIDE = (\n"
            "    'cabinet_member', 'middle_member', 'drawer_member',\n"
            ")\n\n"
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
            "CHILD_ASSEMBLIES = (DRAWER_CHILD,)\n\n"
            + self._hardware_source(
                plan,
                "left",
                mounting.left_runner_translation_mm,
            )
            + self._hardware_source(
                plan,
                "right",
                mounting.right_runner_translation_mm,
            )
            + "PURCHASED_HARDWARE = (RUNNER_LEFT, RUNNER_RIGHT)\n\n"
            "RUNNER_SYSTEM_32_ROWS_MM = "
            f"({mounting.system_32_row_height_mm!r},)\n\n"
            "RUNNER_SIDE_PLACEMENTS = {\n"
            "    'left': "
            + self._placement_source(mounting.left_runner_translation_mm, "    ")
            + ",\n"
            "    'right': "
            + self._placement_source(mounting.right_runner_translation_mm, "    ")
            + ",\n"
            "}\n"
        )

    def _hardware_source(self, plan, hand: str, origin_mm) -> str:
        constant = f"RUNNER_{hand.upper()}"
        return (
            f"{constant} = PurchasedHardwareSpec(\n"
            f"    {plan.drawer.assembly_id + '_runner_' + hand!r},\n"
            f"    {plan.runner.manufacturer!r},\n"
            f"    {plan.runner.product_code!r},\n"
            f"    {plan.runner.asset_id!r},\n"
            "    " + self._placement_source(origin_mm, "    ") + ",\n"
            f"    geometry_selector={hand!r},\n"
            ")\n"
        )

    def _placement_source(
        self,
        origin_mm: tuple[float, float, float],
        indentation: str,
    ) -> str:
        nested = indentation + "    "
        return (
            "LocalToParentPlacement(\n"
            f"{nested}origin_in_parent=Point3D{origin_mm!r},\n"
            f"{nested}axis_basis=AxisBasis(\n"
            f"{nested}    AxisDirection(1.0, 0.0, 0.0),\n"
            f"{nested}    AxisDirection(0.0, 1.0, 0.0),\n"
            f"{nested}    AxisDirection(0.0, 0.0, 1.0),\n"
            f"{nested}),\n"
            f"{indentation})"
        )


__all__ = ["HettichKa5332DrawerInstallationRenderer"]
