"""Scope: Render the builder that composes an existing cabinet and its drawers."""

from __future__ import annotations

from cabinet_drawer_plan import CabinetDrawerPlan


class CabinetWithDrawersBuilderRenderer:
    """Keep parent composition separate from drawer and hardware calculation."""

    def render(self, plan: CabinetDrawerPlan) -> str:
        return (
            f'"""Scope: Build {plan.parent_assembly_id} with its declared drawer children."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltChildAssembly, BuiltPurchasedHardware,\n"
            ")\n\n"
            "from .builder import BUILDER as CABINET_BUILDER\n"
            "from .drawer_installation import CHILD_ASSEMBLIES, FIXED_RUNNERS\n"
            f"from .drawers.{plan.drawer.assembly_id}.builder import BUILDER as DRAWER_BUILDER\n\n\n"
            "class CabinetWithDrawersBuilder:\n"
            "    \"\"\"Compose the existing cabinet and its project-owned drawer child.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        cabinet = CABINET_BUILDER.build()\n"
            "        child = BuiltChildAssembly(CHILD_ASSEMBLIES[0], DRAWER_BUILDER.build())\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            child_assemblies=cabinet.spec.child_assemblies + CHILD_ASSEMBLIES,\n"
            "            purchased_hardware=cabinet.spec.purchased_hardware + FIXED_RUNNERS,\n"
            "        )\n"
            "        runners = tuple(\n"
            "            BuiltPurchasedHardware(spec, None) for spec in FIXED_RUNNERS\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=cabinet.parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies + (child,),\n"
            "            purchased_hardware=cabinet.purchased_hardware + runners,\n"
            "        )\n\n\n"
            "BUILDER = CabinetWithDrawersBuilder()\n"
        )


__all__ = ["CabinetWithDrawersBuilderRenderer"]
