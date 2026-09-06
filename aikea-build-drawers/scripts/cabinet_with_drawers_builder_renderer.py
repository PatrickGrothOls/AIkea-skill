"""Scope: Render the builder that composes an existing cabinet and its drawers."""

from __future__ import annotations

from cabinet_drawer_plan import CabinetDrawerPlan


class CabinetWithDrawersBuilderRenderer:
    """Render a reusable drawer feature over an already-built cabinet."""

    def render(
        self,
        plan: CabinetDrawerPlan,
        hardware_collection: str = "FIXED_RUNNERS",
    ) -> str:
        return (
            f'"""Scope: Apply declared drawers to {plan.parent_assembly_id}."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltChildAssembly, BuiltPurchasedHardware,\n"
            ")\n\n"
            "from ..drawer_installation import CHILD_ASSEMBLIES, "
            f"{hardware_collection}\n"
            f"from .{plan.drawer.assembly_id}.builder import BUILDER as DRAWER_BUILDER\n\n\n"
            "class CabinetDrawerFeature:\n"
            "    \"\"\"Compose the existing cabinet and its project-owned drawer child.\"\"\"\n\n"
            "    def apply(self, cabinet) -> BuiltAssembly:\n"
            "        child = BuiltChildAssembly(CHILD_ASSEMBLIES[0], DRAWER_BUILDER.build())\n"
            "        spec = replace(\n"
            "            cabinet.spec,\n"
            "            child_assemblies=cabinet.spec.child_assemblies + CHILD_ASSEMBLIES,\n"
            "            purchased_hardware=(\n"
            f"                cabinet.spec.purchased_hardware + {hardware_collection}\n"
            "            ),\n"
            "        )\n"
            "        runners = tuple(\n"
            "            BuiltPurchasedHardware(spec, None)\n"
            f"            for spec in {hardware_collection}\n"
            "        )\n"
            "        return BuiltAssembly(\n"
            "            spec=spec, parts=cabinet.parts, joints=cabinet.joints, cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies + (child,),\n"
            "            purchased_hardware=cabinet.purchased_hardware + runners,\n"
            "        )\n\n\n"
            "FEATURE = CabinetDrawerFeature()\n"
        )


__all__ = ["CabinetWithDrawersBuilderRenderer"]
