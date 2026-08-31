"""Scope: Coordinate generated files for one cabinet's KA 5332 drawers."""

from __future__ import annotations

from pathlib import Path

from cabinet_feature_builder_wrapper_renderer import (
    CabinetFeatureBuilderWrapperRenderer,
)
from hettich_ka_5332_cabinet_drawers_builder_renderer import (
    HettichKa5332CabinetDrawersBuilderRenderer,
)
from hettich_ka_5332_cabinet_drawers_plan import (
    HettichKa5332CabinetDrawersPlan,
)
from hettich_ka_5332_drawers_installation_renderer import (
    HettichKa5332DrawersInstallationRenderer,
)
from hettich_ka_5332_drawers_layout_renderer import (
    HettichKa5332DrawersLayoutRenderer,
)
from wooden_drawer_child_module_renderer import WoodenDrawerChildModuleRenderer


class HettichKa5332DrawersFileSetRenderer:
    """Route a drawer collection into cabinet and child-owned modules."""

    def __init__(self) -> None:
        self.layout = HettichKa5332DrawersLayoutRenderer()
        self.installation = HettichKa5332DrawersInstallationRenderer()
        self.cabinet_builder = HettichKa5332CabinetDrawersBuilderRenderer()
        self.wrapper = CabinetFeatureBuilderWrapperRenderer()
        self.drawer_child = WoodenDrawerChildModuleRenderer()

    def render(self, plan: HettichKa5332CabinetDrawersPlan) -> dict[Path, str]:
        parent = Path("assemblies") / plan.parent_assembly_id
        files = {
            parent / "drawer-layout.yaml": self.layout.render(plan),
            parent / "drawers/__init__.py": (
                f'"""Scope: Contain drawer children owned by {plan.parent_assembly_id}."""\n'
            ),
            parent / "drawer_installation.py": self.installation.render(plan),
            parent / "drawers/feature.py": self.cabinet_builder.render(plan),
            parent / "with_drawers_builder.py": self.wrapper.render(
                plan.parent_assembly_id,
                "drawers.feature",
            ),
        }
        for drawer in plan.drawers:
            root = parent / "drawers" / drawer.drawer.assembly_id
            files.update(self.drawer_child.render(root, drawer))
        return files


__all__ = ["HettichKa5332DrawersFileSetRenderer"]
