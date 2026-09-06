"""Scope: Render every KA 5332 drawer frame and runner pair in one cabinet."""

from __future__ import annotations

from hettich_ka_5332_cabinet_drawers_plan import (
    HettichKa5332CabinetDrawersPlan,
)


class HettichKa5332DrawersInstallationRenderer:
    """Save independent child frames and purchased hardware per drawer."""

    def render(self, plan: HettichKa5332CabinetDrawersPlan) -> str:
        children = ",\n".join(
            self._child_source(drawer) for drawer in plan.drawers
        )
        hardware = ",\n".join(
            self._hardware_source(drawer) for drawer in plan.drawers
        )
        placements = ",\n".join(
            self._runner_placements_source(drawer) for drawer in plan.drawers
        )
        rows = ", ".join(
            repr(drawer.hardware_mounting.system_32_row_height_mm)
            for drawer in plan.drawers
        )
        return (
            f'"""Scope: Place drawers and runner hardware owned by {plan.parent_assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, ChildAssemblySpec, LocalToParentPlacement,\n"
            "    Point3D, PurchasedHardwareSpec,\n"
            ")\n\n\n"
            "SOURCE_MEMBERS_PER_SIDE = (\n"
            "    'cabinet_member', 'middle_member', 'drawer_member',\n"
            ")\n\n"
            f"CHILD_ASSEMBLIES = (\n{children},\n)\n\n"
            f"PURCHASED_HARDWARE = (\n{hardware},\n)\n\n"
            f"RUNNER_SYSTEM_32_ROWS_MM = ({rows},)\n\n"
            f"RUNNER_SIDE_PLACEMENTS = {{\n{placements},\n}}\n"
        )

    def _child_source(self, drawer) -> str:
        x_mm, y_mm, z_mm = drawer.origin_in_parent_mm
        return (
            "    ChildAssemblySpec(\n"
            f"        assembly_id={drawer.drawer.assembly_id!r},\n"
            "        purpose='drawer',\n"
            "        local_to_parent=LocalToParentPlacement(\n"
            f"            origin_in_parent=Point3D({x_mm!r}, {y_mm!r}, {z_mm!r}),\n"
            f"            axis_basis={self._axis_basis_source('            ')},\n"
            "        ),\n"
            "    )"
        )

    def _hardware_source(self, drawer) -> str:
        mounting = drawer.hardware_mounting
        left = self._runner_hardware_source(
            drawer,
            "left",
            mounting.left_runner_translation_mm,
        )
        right = self._runner_hardware_source(
            drawer,
            "right",
            mounting.right_runner_translation_mm,
        )
        return f"{left},\n{right}"

    def _runner_hardware_source(self, drawer, hand: str, origin_mm) -> str:
        return (
            "    PurchasedHardwareSpec(\n"
            f"        {drawer.drawer.assembly_id + '_runner_' + hand!r},\n"
            f"        {drawer.runner.manufacturer!r},\n"
            f"        {drawer.runner.product_code!r},\n"
            f"        {drawer.runner.asset_id!r},\n"
            "        " + self._placement_source(origin_mm, "        ") + ",\n"
            f"        geometry_selector={hand!r},\n"
            "    )"
        )

    def _runner_placements_source(self, drawer) -> str:
        mounting = drawer.hardware_mounting
        return (
            f"    {drawer.drawer.assembly_id!r}: {{\n"
            "        'left': "
            + self._placement_source(mounting.left_runner_translation_mm, "        ")
            + ",\n"
            "        'right': "
            + self._placement_source(mounting.right_runner_translation_mm, "        ")
            + ",\n"
            "    }"
        )

    def _placement_source(self, origin_mm, indentation: str) -> str:
        nested = indentation + "    "
        return (
            "LocalToParentPlacement(\n"
            f"{nested}origin_in_parent=Point3D{origin_mm!r},\n"
            f"{nested}axis_basis={self._axis_basis_source(nested)},\n"
            f"{indentation})"
        )

    def _axis_basis_source(self, indentation: str) -> str:
        nested = indentation + "    "
        return (
            "AxisBasis(\n"
            f"{nested}AxisDirection(1.0, 0.0, 0.0),\n"
            f"{nested}AxisDirection(0.0, 1.0, 0.0),\n"
            f"{nested}AxisDirection(0.0, 0.0, 1.0),\n"
            f"{indentation})"
        )


__all__ = ["HettichKa5332DrawersInstallationRenderer"]
