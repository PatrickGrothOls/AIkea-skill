"""Scope: Render the unmachined wooden child used by the KA 4532 proof."""

from __future__ import annotations

from pathlib import Path

from drawer_box_spec_source_renderer import DrawerBoxSpecSourceRenderer


class HettichKa4532SpacerDrawerChildRenderer:
    """Build review geometry while the explicit machining gate remains closed."""

    def __init__(self) -> None:
        self.box = DrawerBoxSpecSourceRenderer()

    def render(self, root: Path, plan) -> dict[Path, str]:
        return {
            root / "__init__.py": (
                f'"""Scope: Contain the {plan.drawer.assembly_id} child assembly."""\n'
            ),
            root / "spec.py": self._spec(plan),
            root / "builder.py": self._builder(plan.drawer.assembly_id),
        }

    def _spec(self, plan) -> str:
        return (
            f'"""Scope: Own the resolved {plan.drawer.assembly_id} dimensions."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n"
            ")\n"
            "from drawer_assembly_spec import DrawerAssemblySpec\n"
            "from drawer_box_spec import (\n"
            "    CabinetDrawerOpening, DrawerBoxSizingProfile, DrawerBoxSpec, DrawerPartSpec,\n"
            ")\n\n"
            "from ...drawer_installation import DRAWER_HARDWARE\n\n\n"
            f"BOX_SPEC = {self.box.render(plan.drawer.box)}\n\n"
            "SPEC = DrawerAssemblySpec(\n"
            f"    assembly_id={plan.drawer.assembly_id!r},\n"
            "    purpose='drawer',\n"
            f"    runner_product_code={plan.hardware.runner_product_code!r},\n"
            f"    runner_item_number={plan.hardware.runner_item_number!r},\n"
            f"    hardware_geometry_state={plan.drawer.hardware_geometry_state!r},\n"
            "    box=BOX_SPEC,\n"
            "    purchased_hardware=DRAWER_HARDWARE,\n"
            ")\n"
        )

    def _builder(self, drawer_id: str) -> str:
        class_name = "".join(part.capitalize() for part in drawer_id.split("_"))
        return (
            f'"""Scope: Build the review-only wooden sheets owned by {drawer_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltPart, BuiltPurchasedHardware,\n"
            ")\n"
            "from drawer_box_builder import DrawerBoxBuilder\n\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}Builder:\n"
            "    \"\"\"Build blanks without claiming unresolved fixing machining.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        box = DrawerBoxBuilder().build(SPEC.box)\n"
            "        parts = tuple(BuiltPart(part.spec, part.solid) for part in box.parts)\n"
            "        hardware = tuple(\n"
            "            BuiltPurchasedHardware(spec, None)\n"
            "            for spec in SPEC.purchased_hardware\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            SPEC, parts, (), purchased_hardware=hardware\n"
            "        )\n\n\n"
            f"BUILDER = {class_name}Builder()\n"
        )


__all__ = ["HettichKa4532SpacerDrawerChildRenderer"]
