"""Scope: Render one wooden drawer child without vendor-specific hardware."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from drawer_box_spec_source_renderer import DrawerBoxSpecSourceRenderer
from drawer_construction_module_renderer import DrawerConstructionModuleRenderer
from hettich_ka_5332_drilling_recipe import HettichKa5332DrillingRecipe
from surface_drilling_source_renderer import SurfaceDrillingSourceRenderer


class WoodenDrawerChildModuleRenderer:
    """Create an importable five-sheet drawer child from a resolved plan."""

    def __init__(self) -> None:
        self.box_renderer = DrawerBoxSpecSourceRenderer()

    def render(self, root: Path, plan: Any) -> dict[Path, str]:
        return {
            root / "__init__.py": (
                f'"""Scope: Contain the {plan.drawer.assembly_id} child assembly."""\n'
            ),
            root / "spec.py": self._spec(plan),
            root / "builder.py": self._builder(plan),
        }

    def _spec(self, plan: Any) -> str:
        box = self.box_renderer.render(plan.drawer.box)
        drilling = HettichKa5332DrillingRecipe().drawer(plan.drawer.box, plan.runner)
        requests = "\n".join(f"        {SurfaceDrillingSourceRenderer().render(request)}," for request in drilling)
        return (
            f'"""Scope: Own the resolved {plan.drawer.assembly_id} dimensions."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, LocalToParentPlacement, Point3D,\n"
            "    BoundaryPoint, ConstructionRequirementSpec, SurfaceDrillingSpec,\n"
            ")\n"
            "from drawer_assembly_spec import DrawerAssemblySpec\n"
            "from surface_hole_pattern import SurfaceHole\n"
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
            f"    machining=(\n{requests}\n    ),\n"
            f"{DrawerConstructionModuleRenderer().requirements(plan.drawer.box, drilling)}"
            ")\n"
        )

    def _builder(self, plan: Any) -> str:
        return DrawerConstructionModuleRenderer().builder(plan.drawer.assembly_id)


__all__ = ["WoodenDrawerChildModuleRenderer"]
