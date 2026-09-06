"""Scope: Render local project files for one cabinet-owned recessed light."""

from __future__ import annotations

from pathlib import Path

import yaml

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
            host / "lighting.yaml": yaml.safe_dump(plan.as_record(), sort_keys=False),
            host / "lighting.py": self._plan_module(plan),
            host / "lighting_builder.py": self._part_builder_module(plan),
            assembly / "lighting/__init__.py": (
                f'"""Scope: Contain lighting features owned by {plan.assembly_id}."""\n'
            ),
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
            f'"""Scope: Apply the declared recessed light to {plan.assembly_id}."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltPurchasedHardware, PurchasedHardwareSpec,\n"
            ")\n"
            "from cabinet_lighting_placement import CabinetLightingPlacementBuilder\n\n"
            f"from ..parts.{plan.part_id}.lighting import PLAN\n"
            f"from ..parts.{plan.part_id}.lighting_builder import BUILDER as LIGHTING_BUILDER\n\n\n"
            "class CabinetLightingFeature:\n"
            "    \"\"\"Compose the machined host part and one purchased luminaire.\"\"\"\n\n"
            "    def apply(self, cabinet) -> BuiltAssembly:\n"
            "        host = next(part for part in cabinet.parts if part.spec.part_id == PLAN.part_id)\n"
            "        lighting = LIGHTING_BUILDER.build(host)\n"
            "        placement = CabinetLightingPlacementBuilder().build(\n"
            "            cabinet.spec, host.spec, PLAN\n"
            "        )\n"
            "        hardware_spec = PurchasedHardwareSpec(\n"
            "            PLAN.run.run_id,\n"
            "            PLAN.run.profile.manufacturer,\n"
            "            PLAN.run.profile.product_name,\n"
            "            PLAN.run.profile.profile_id,\n"
            "            placement.luminaire_in_cabinet.as_project_placement(),\n"
            "        )\n"
            "        parts = tuple(\n"
            "            lighting.part if part.spec.part_id == PLAN.part_id else part\n"
            "            for part in cabinet.parts\n"
            "        )\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            purchased_hardware=cabinet.spec.purchased_hardware + (hardware_spec,),\n"
            "        )\n"
            "        hardware = BuiltPurchasedHardware(hardware_spec, lighting.luminaire_body)\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies,\n"
            "            purchased_hardware=cabinet.purchased_hardware + (hardware,),\n"
            "        )\n\n\n"
            "FEATURE = CabinetLightingFeature()\n"
        )

    def _wrapper_module(
        self,
        plan: PartLightingPlan,
        base_builder_module: str,
    ) -> str:
        return (
            f'"""Scope: Build {plan.assembly_id} with its recessed light."""\n\n'
            "from assemblies.assembly_feature import FeatureComposedAssemblyBuilder\n\n"
            f"from .{base_builder_module} import BUILDER as BASE_BUILDER\n"
            "from .lighting.feature import FEATURE\n\n\n"
            "BUILDER = FeatureComposedAssemblyBuilder(BASE_BUILDER, (FEATURE,))\n"
        )


__all__ = ["CabinetLightingFileSetRenderer"]
