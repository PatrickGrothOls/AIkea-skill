"""Scope: Render one resolved drawer child's own specification and builder."""

from __future__ import annotations

from pathlib import Path

from cabinet_drawer_plan import CabinetDrawerPlan
from drawer_box_spec_source_renderer import DrawerBoxSpecSourceRenderer
from hardware_placement_renderer import HardwarePlacementRenderer
from drawer_construction_module_renderer import DrawerConstructionModuleRenderer


class DrawerChildModuleRenderer:
    """Create one importable drawer child without parent-cabinet concerns."""

    def __init__(self) -> None:
        self.box_renderer = DrawerBoxSpecSourceRenderer()
        self.placement_renderer = HardwarePlacementRenderer()

    def render(self, root: Path, plan: CabinetDrawerPlan) -> dict[Path, str]:
        return {
            root / "__init__.py": (
                f'"""Scope: Contain the {plan.drawer.assembly_id} child assembly."""\n'
            ),
            root / "spec.py": self._spec(plan),
            root / "builder.py": self._builder(plan),
        }

    def _spec(self, plan: CabinetDrawerPlan) -> str:
        box = self.box_renderer.render(plan.drawer.box)
        hardware = plan.runner.require_hardware_asset_set()
        mounting = plan.hardware_mounting
        return (
            f'"""Scope: Own the resolved {plan.drawer.assembly_id} dimensions."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n"
            "    PurchasedHardwareSpec,\n"
            "    BoundaryPoint, ConstructionRequirementSpec,\n"
            ")\n"
            "from drawer_assembly_spec import DrawerAssemblySpec\n"
            "from drawer_box_spec import (\n"
            "    CabinetDrawerOpening, DrawerBoxSizingProfile, DrawerBoxSpec, DrawerPartSpec,\n"
            ")\n\n\n"
            f"BOX_SPEC = {box}\n\n"
            "LOCKING_DEVICES = (\n"
            "    PurchasedHardwareSpec(\n"
            f"        'locking_device_left', 'Blum', "
            f"{hardware.locking_device_left.product_code!r},\n"
            f"        {hardware.locking_device_left.asset_id!r},\n"
            "        local_to_parent="
            + self.placement_renderer.render(
                mounting.locking_device_left_in_drawer,
                "        ",
            )
            + ",\n"
            "    ),\n"
            "    PurchasedHardwareSpec(\n"
            f"        'locking_device_right', 'Blum', "
            f"{hardware.locking_device_right.product_code!r},\n"
            f"        {hardware.locking_device_right.asset_id!r},\n"
            "        local_to_parent="
            + self.placement_renderer.render(
                mounting.locking_device_right_in_drawer,
                "        ",
            )
            + ",\n"
            "    ),\n"
            ")\n\n"
            "SPEC = DrawerAssemblySpec(\n"
            f"    assembly_id={plan.drawer.assembly_id!r},\n"
            "    purpose='drawer',\n"
            f"    runner_product_code={plan.runner.product_code!r},\n"
            f"    runner_item_number={plan.runner.item_number!r},\n"
            f"    hardware_geometry_state={plan.drawer.hardware_geometry_state!r},\n"
            "    box=BOX_SPEC,\n"
            "    purchased_hardware=LOCKING_DEVICES,\n"
            "    machining=(),\n"
            f"{DrawerConstructionModuleRenderer().requirements(plan.drawer.box, hardware_ids=('locking_device_left', 'locking_device_right'))}"
            ")\n"
        )

    def _builder(self, plan: CabinetDrawerPlan) -> str:
        return DrawerConstructionModuleRenderer().builder(plan.drawer.assembly_id)


__all__ = ["DrawerChildModuleRenderer"]
