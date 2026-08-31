"""Scope: Coordinate the generated file set owned by one cabinet drawer addition."""

from __future__ import annotations

from pathlib import Path

from cabinet_feature_builder_wrapper_renderer import (
    CabinetFeatureBuilderWrapperRenderer,
)
from cabinet_drawer_plan import CabinetDrawerPlan
from cabinet_with_drawers_builder_renderer import (
    CabinetWithDrawersBuilderRenderer,
)
from drawer_child_module_renderer import DrawerChildModuleRenderer
from drawer_installation_renderer import DrawerInstallationRenderer
from drawer_layout_renderer import DrawerLayoutRenderer


class CabinetDrawerFileSetRenderer:
    """Route each generated drawer file to its one-purpose renderer."""

    def __init__(self) -> None:
        self.layout = DrawerLayoutRenderer()
        self.installation = DrawerInstallationRenderer()
        self.parent_builder = CabinetWithDrawersBuilderRenderer()
        self.wrapper = CabinetFeatureBuilderWrapperRenderer()
        self.drawer_child = DrawerChildModuleRenderer()

    def render(self, plan: CabinetDrawerPlan) -> dict[Path, str]:
        parent = Path("assemblies") / plan.parent_assembly_id
        drawer = parent / "drawers" / plan.drawer.assembly_id
        files = {
            parent / "drawer-layout.yaml": self.layout.render(plan),
            parent / "drawers/__init__.py": (
                f'"""Scope: Contain drawer children owned by {plan.parent_assembly_id}."""\n'
            ),
            parent / "drawer_installation.py": self.installation.render(plan),
            parent / "drawers/feature.py": self.parent_builder.render(plan),
            parent / "with_drawers_builder.py": self.wrapper.render(
                plan.parent_assembly_id,
                "drawers.feature",
            ),
        }
        files.update(self.drawer_child.render(drawer, plan))
        return files


__all__ = ["CabinetDrawerFileSetRenderer"]
