"""Scope: Coordinate files generated for one cabinet's KA 5332 drawer."""

from __future__ import annotations

from pathlib import Path

from hettich_ka_5332_cabinet_builder_renderer import (
    HettichKa5332CabinetBuilderRenderer,
)
from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
)
from hettich_ka_5332_drawer_installation_renderer import (
    HettichKa5332DrawerInstallationRenderer,
)
from hettich_ka_5332_drawer_layout_renderer import (
    HettichKa5332DrawerLayoutRenderer,
)
from wooden_drawer_child_module_renderer import WoodenDrawerChildModuleRenderer


class HettichKa5332DrawerFileSetRenderer:
    """Route Hettich planning data into cabinet and child-owned modules."""

    def __init__(self) -> None:
        self.layout = HettichKa5332DrawerLayoutRenderer()
        self.installation = HettichKa5332DrawerInstallationRenderer()
        self.cabinet_builder = HettichKa5332CabinetBuilderRenderer()
        self.drawer_child = WoodenDrawerChildModuleRenderer()

    def render(
        self,
        plan: HettichKa5332CabinetDrawerPlan,
    ) -> dict[Path, str]:
        parent = Path("assemblies") / plan.parent_assembly_id
        drawer = parent / "drawers" / plan.drawer.assembly_id
        files = {
            parent / "drawer-layout.yaml": self.layout.render(plan),
            parent / "drawers/__init__.py": (
                f'"""Scope: Contain drawer children owned by {plan.parent_assembly_id}."""\n'
            ),
            parent / "drawer_installation.py": self.installation.render(plan),
            parent / "with_drawers_builder.py": self.cabinet_builder.render(plan),
        }
        files.update(self.drawer_child.render(drawer, plan))
        return files


__all__ = ["HettichKa5332DrawerFileSetRenderer"]
