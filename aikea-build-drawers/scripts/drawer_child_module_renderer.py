"""Scope: Render one resolved drawer child's own specification and builder."""

from __future__ import annotations

from pathlib import Path
from pprint import pformat

from cabinet_drawer_plan import CabinetDrawerPlan


class DrawerChildModuleRenderer:
    """Create one importable drawer child without parent-cabinet concerns."""

    def render(self, root: Path, plan: CabinetDrawerPlan) -> dict[Path, str]:
        return {
            root / "__init__.py": (
                f'"""Scope: Contain the {plan.drawer.assembly_id} child assembly."""\n'
            ),
            root / "spec.py": self._spec(plan),
            root / "builder.py": self._builder(plan),
        }

    def _spec(self, plan: CabinetDrawerPlan) -> str:
        box = pformat(plan.drawer.box, width=88, sort_dicts=False)
        return (
            f'"""Scope: Own the resolved {plan.drawer.assembly_id} dimensions."""\n\n'
            "from drawer_assembly_spec import DrawerAssemblySpec\n"
            "from drawer_box_spec import (\n"
            "    CabinetDrawerOpening, DrawerBoxSizingProfile, DrawerBoxSpec, DrawerPartSpec,\n"
            ")\n\n\n"
            f"BOX_SPEC = {box}\n\n"
            "SPEC = DrawerAssemblySpec(\n"
            f"    assembly_id={plan.drawer.assembly_id!r},\n"
            "    purpose='drawer',\n"
            f"    runner_product_code={plan.runner.product_code!r},\n"
            f"    runner_item_number={plan.runner.item_number!r},\n"
            f"    hardware_geometry_state={plan.drawer.hardware_geometry_state!r},\n"
            "    box=BOX_SPEC,\n"
            ")\n"
        )

    def _builder(self, plan: CabinetDrawerPlan) -> str:
        class_name = "".join(
            part.capitalize() for part in plan.drawer.assembly_id.split("_")
        )
        return (
            f'"""Scope: Build every wooden sheet owned by {plan.drawer.assembly_id}."""\n\n'
            "from assemblies.specification import BuiltAssembly, BuiltPart\n"
            "from drawer_box_builder import DrawerBoxBuilder\n\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}Builder:\n"
            "    \"\"\"Build the resolved drawer box in canonical part frames.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        box = DrawerBoxBuilder().build(SPEC.box)\n"
            "        parts = tuple(BuiltPart(part.spec, part.solid) for part in box.parts)\n"
            "        return BuiltAssembly(SPEC, parts, ())\n\n\n"
            f"BUILDER = {class_name}Builder()\n"
        )


__all__ = ["DrawerChildModuleRenderer"]
