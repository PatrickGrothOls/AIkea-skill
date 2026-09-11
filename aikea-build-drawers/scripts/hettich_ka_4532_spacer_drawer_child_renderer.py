"""Scope: Render the unmachined wooden child used by the KA 4532 proof."""

from __future__ import annotations

from pathlib import Path

from drawer_box_spec_source_renderer import DrawerBoxSpecSourceRenderer
from drawer_construction_module_renderer import DrawerConstructionModuleRenderer


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
        hardware_ids = tuple(f"{plan.drawer.assembly_id}_runner_{side}_moving" for side in ("left", "right"))
        return (
            f'"""Scope: Own the resolved {plan.drawer.assembly_id} dimensions."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n"
            "    BoundaryPoint, ConstructionRequirementSpec,\n"
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
            "    machining=(),\n"
            f"{DrawerConstructionModuleRenderer().requirements(plan.drawer.box, hardware_ids=hardware_ids)}"
            ")\n"
        )

    def _builder(self, drawer_id: str) -> str:
        return DrawerConstructionModuleRenderer().builder(drawer_id)


__all__ = ["HettichKa4532SpacerDrawerChildRenderer"]
