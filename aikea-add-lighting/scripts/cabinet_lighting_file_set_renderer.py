"""Scope: Render local project files for one cabinet-owned recessed light."""

from __future__ import annotations

from pathlib import Path

import yaml

from complete_assembly_builder_renderer import CompleteAssemblyBuilderRenderer
from part_lighting_plan import PartLightingPlan


class CabinetLightingFileSetRenderer:
    """Keep source data with its host part and composition with its cabinet."""

    def render(
        self,
        plan: PartLightingPlan,
        base_builder_module: str,
    ) -> dict[Path, str]:
        assembly = Path("assemblies") / plan.assembly_id
        host = assembly / "parts" / plan.part_id
        return {
            assembly / "complete_builder.py": CompleteAssemblyBuilderRenderer().render(plan.assembly_id),
            host / "lighting.yaml": yaml.safe_dump(plan.as_record(), sort_keys=False),
            host / "lighting.py": self._plan_module(plan),
            host / "lighting_builder.py": self._part_builder_module(plan),
            assembly / "lighting/__init__.py": (
                f'"""Scope: Contain lighting features owned by {plan.assembly_id}."""\n'
            ),
            assembly / "lighting/review.py": self._review_module(plan),
            assembly / "lighting/feature.py": self._assembly_feature_module(plan),
            assembly / "with_lighting_builder.py": self._wrapper_module(
                plan,
                base_builder_module,
            ),
        }

    def _plan_module(self, plan: PartLightingPlan) -> str:
        return (
            f'"""Scope: Load the saved recessed-light plan for {plan.part_id}."""\n\n'
            "from pathlib import Path\n"
            "from part_lighting_plan_loader import PartLightingPlanLoader\n\n\n"
            "PLAN = PartLightingPlanLoader().load(Path(__file__).with_name(\"lighting.yaml\"))\n"
        )

    def _part_builder_module(self, plan: PartLightingPlan) -> str:
        return (
            f'"""Scope: Apply saved recessed lighting to {plan.part_id}."""\n\n'
            "from part_lighting_builder import PartLightingBuilder\n\n"
            "from .lighting import PLAN\n\n\n"
            "class HostPartLightingBuilder:\n"
            "    \"\"\"Cut the saved groove into the already-machined host part.\"\"\"\n\n"
            "    def build(self, built_part):\n"
            "        return PartLightingBuilder().build(built_part, PLAN)\n\n\n"
            "BUILDER = HostPartLightingBuilder()\n"
        )

    def _assembly_feature_module(self, plan: PartLightingPlan) -> str:
        return (
            f'"""Scope: Apply the saved lighting feature owned by {plan.assembly_id}."""\n\n'
            "from lighting_component_feature import LightingComponentFeature\n"
            f"from ..parts.{plan.part_id}.lighting import PLAN\n\n"
            "FEATURE = LightingComponentFeature(PLAN)\n"
        )

    def _review_module(self, plan):
        return (
            '"""Scope: Contribute the owned lighting to generic assembly review."""\n'
            'from lighting_component_review import LightingComponentReview\n'
            f'from ..parts.{plan.part_id}.lighting import PLAN\n'
            'REVIEW = LightingComponentReview(PLAN)\n'
        )

    def _wrapper_module(self, plan, base_builder_module):
        return (
            f'"""Scope: Retain the complete assembly as the lighting review authority."""\n'
            "from .complete_builder import BUILDER\n"
        )


__all__ = ["CabinetLightingFileSetRenderer"]
