"""Scope: Render a cabinet builder that composes its KA 5332 drawer child."""

from __future__ import annotations

from hettich_ka_5332_cabinet_drawer_plan import (
    HettichKa5332CabinetDrawerPlan,
)


class HettichKa5332CabinetBuilderRenderer:
    """Compose existing cabinet geometry, one drawer, and one purchased pair."""

    def render(self, plan: HettichKa5332CabinetDrawerPlan) -> str:
        return (
            f'"""Scope: Build {plan.parent_assembly_id} with its declared drawer child."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltChildAssembly, BuiltPurchasedHardware,\n"
            ")\n\n"
            "from .builder import BUILDER as CABINET_BUILDER\n"
            "from .drawer_installation import CHILD_ASSEMBLIES, PURCHASED_HARDWARE\n"
            f"from .drawers.{plan.drawer.assembly_id}.builder import BUILDER as DRAWER_BUILDER\n\n\n"
            "class CabinetWithDrawersBuilder:\n"
            "    \"\"\"Compose the existing cabinet and its project-owned drawer child.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        cabinet = CABINET_BUILDER.build()\n"
            "        child = BuiltChildAssembly(CHILD_ASSEMBLIES[0], DRAWER_BUILDER.build())\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            child_assemblies=cabinet.spec.child_assemblies + CHILD_ASSEMBLIES,\n"
            "            purchased_hardware=(\n"
            "                cabinet.spec.purchased_hardware + PURCHASED_HARDWARE\n"
            "            ),\n"
            "        )\n"
            "        hardware = tuple(\n"
            "            BuiltPurchasedHardware(item, None)\n"
            "            for item in PURCHASED_HARDWARE\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=cabinet.parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies + (child,),\n"
            "            purchased_hardware=cabinet.purchased_hardware + hardware,\n"
            "        )\n\n\n"
            "BUILDER = CabinetWithDrawersBuilder()\n"
        )


__all__ = ["HettichKa5332CabinetBuilderRenderer"]
