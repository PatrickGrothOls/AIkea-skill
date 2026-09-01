"""Scope: Coordinate one generated KA 4532 spacer drawer file set."""

from __future__ import annotations

from pathlib import Path

from cabinet_feature_builder_wrapper_renderer import (
    CabinetFeatureBuilderWrapperRenderer,
)
from cabinet_with_drawers_builder_renderer import (
    CabinetWithDrawersBuilderRenderer,
)
from hettich_ka_4532_spacer_drawer_child_renderer import (
    HettichKa4532SpacerDrawerChildRenderer,
)
from hettich_ka_4532_spacer_installation_renderer import (
    HettichKa4532SpacerInstallationRenderer,
)
from hettich_ka_4532_spacer_layout_renderer import (
    HettichKa4532SpacerLayoutRenderer,
)
from hettich_ka_4532_spacer_machining_authority_renderer import (
    HettichKa4532SpacerMachiningAuthorityRenderer,
)
from hettich_ka_4532_spacer_review_module_renderer import (
    HettichKa4532SpacerReviewModuleRenderer,
)


class HettichKa4532SpacerFileSetRenderer:
    """Route each saved concern to one project-owned module or evidence record."""

    def __init__(self) -> None:
        self.layout = HettichKa4532SpacerLayoutRenderer()
        self.installation = HettichKa4532SpacerInstallationRenderer()
        self.child = HettichKa4532SpacerDrawerChildRenderer()
        self.feature = CabinetWithDrawersBuilderRenderer()
        self.wrapper = CabinetFeatureBuilderWrapperRenderer()
        self.machining = HettichKa4532SpacerMachiningAuthorityRenderer()
        self.review = HettichKa4532SpacerReviewModuleRenderer()

    def render(self, plan) -> dict[Path, str]:
        parent = Path("assemblies") / plan.parent_assembly_id
        drawers = parent / "drawers"
        child = drawers / plan.drawer.assembly_id
        files = {
            parent / "drawer-layout.yaml": self.layout.render(plan),
            parent / "drawer_installation.py": self.installation.render(plan),
            drawers / "__init__.py": (
                f'"""Scope: Contain drawer features owned by {plan.parent_assembly_id}."""\n'
            ),
            drawers / "feature.py": self.feature.render(plan, "CABINET_HARDWARE"),
            drawers / "review.py": self.review.render(plan),
            drawers / "machining-authority.json": self.machining.render(plan),
            parent / "with_drawers_builder.py": self.wrapper.render(
                plan.parent_assembly_id,
                "drawers.feature",
            ),
        }
        files.update(self.child.render(child, plan))
        return files


__all__ = ["HettichKa4532SpacerFileSetRenderer"]
