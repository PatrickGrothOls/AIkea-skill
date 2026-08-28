"""Scope: Render one project-owned drawer child and its cabinet composition."""

from __future__ import annotations

from pathlib import Path

import yaml

from cabinet_drawer_plan import CabinetDrawerPlan
from drawer_child_module_renderer import DrawerChildModuleRenderer


class CabinetDrawerModuleRenderer:
    """Create the local files that make one drawer a built cabinet child."""

    def __init__(self) -> None:
        self.drawer_child = DrawerChildModuleRenderer()

    def render(self, plan: CabinetDrawerPlan) -> dict[Path, str]:
        parent = Path("assemblies") / plan.parent_assembly_id
        drawer = parent / "drawers" / plan.drawer.assembly_id
        files = {
            parent / "drawer-layout.yaml": self._layout(plan),
            parent / "drawers/__init__.py": self._package(
                f"Contain drawer children owned by {plan.parent_assembly_id}"
            ),
            parent / "drawer_installation.py": self._installation(plan),
            parent / "with_drawers_builder.py": self._parent_builder(plan),
        }
        files.update(self.drawer_child.render(drawer, plan))
        return files

    def _layout(self, plan: CabinetDrawerPlan) -> str:
        layout = plan.layout
        x_mm, y_mm, z_mm = plan.origin_in_parent_mm
        data = {
            "schema_version": 1,
            "parent_assembly_id": plan.parent_assembly_id,
            "drawers": [
                {
                    "id": layout.drawer_id,
                    "bottom_height_mm": layout.bottom_height_mm,
                    "box": {
                        "height_mm": layout.box_height_mm,
                        "side_thickness_mm": layout.side_thickness_mm,
                        "front_back_thickness_mm": layout.front_back_thickness_mm,
                        "bottom_thickness_mm": layout.bottom_thickness_mm,
                        "bottom_underside_recess_mm": (
                            layout.bottom_underside_recess_mm
                        ),
                    },
                    "runner": {
                        "manufacturer": "Blum",
                        "assembly_owner": plan.parent_assembly_id,
                        "product_code": plan.runner.product_code,
                        "item_number": plan.runner.item_number,
                        "nominal_length_mm": plan.runner.nominal_length_mm,
                        "geometry": plan.drawer.hardware_geometry_state,
                    },
                    "local_frame": {
                        "origin_in_parent_mm": {"x": x_mm, "y": y_mm, "z": z_mm},
                        "local_x_in_parent": [1.0, 0.0, 0.0],
                        "local_y_in_parent": [0.0, 1.0, 0.0],
                        "local_z_in_parent": [0.0, 0.0, 1.0],
                    },
                }
            ],
        }
        return yaml.safe_dump(data, sort_keys=False)

    def _installation(self, plan: CabinetDrawerPlan) -> str:
        runner_assets = plan.runner.runner_asset_pair
        if runner_assets is None:
            raise ValueError(
                f"{plan.runner.product_code} has no complete handed CAD pair"
            )
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
            "    PurchasedHardwareSpec(\n"
            f"        'runner_left', 'Blum', {plan.runner.product_code!r},\n"
            f"        {runner_assets.left_asset_id!r}, None,\n"
            "    ),\n"
            "    PurchasedHardwareSpec(\n"
            f"        'runner_right', 'Blum', {plan.runner.product_code!r},\n"
            f"        {runner_assets.right_asset_id!r}, None,\n"
            "    ),\n"
            ")\n"
        )

    def _parent_builder(self, plan: CabinetDrawerPlan) -> str:
        return (
            f'"""Scope: Build {plan.parent_assembly_id} with its declared drawer children."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltChildAssembly, BuiltPurchasedHardware,\n"
            ")\n\n"
            "from .builder import BUILDER as CABINET_BUILDER\n"
            "from .drawer_installation import CHILD_ASSEMBLIES, FIXED_RUNNERS\n"
            f"from .drawers.{plan.drawer.assembly_id}.builder import BUILDER as DRAWER_BUILDER\n\n\n"
            "class CabinetWithDrawersBuilder:\n"
            "    \"\"\"Compose the existing cabinet and its project-owned drawer child.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        cabinet = CABINET_BUILDER.build()\n"
            "        child = BuiltChildAssembly(CHILD_ASSEMBLIES[0], DRAWER_BUILDER.build())\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            child_assemblies=cabinet.spec.child_assemblies + CHILD_ASSEMBLIES,\n"
            "            purchased_hardware=cabinet.spec.purchased_hardware + FIXED_RUNNERS,\n"
            "        )\n"
            "        runners = tuple(\n"
            "            BuiltPurchasedHardware(spec, None) for spec in FIXED_RUNNERS\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=cabinet.parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies + (child,),\n"
            "            purchased_hardware=cabinet.purchased_hardware + runners,\n"
            "        )\n\n\n"
            "BUILDER = CabinetWithDrawersBuilder()\n"
        )

    def _package(self, responsibility: str) -> str:
        return f'"""Scope: {responsibility}."""\n'


__all__ = ["CabinetDrawerModuleRenderer"]
