"""Scope: Render a cabinet builder that composes any number of drawers."""

from __future__ import annotations

from hettich_ka_5332_cabinet_drawers_plan import (
    HettichKa5332CabinetDrawersPlan,
)


class HettichKa5332CabinetDrawersBuilderRenderer:
    """Compose existing cabinet geometry with every declared drawer child."""

    def render(self, plan: HettichKa5332CabinetDrawersPlan) -> str:
        imports = "\n".join(
            self._builder_import(drawer.drawer.assembly_id)
            for drawer in plan.drawers
        )
        builders = ", ".join(
            self._builder_name(drawer.drawer.assembly_id)
            for drawer in plan.drawers
        )
        return (
            f'"""Scope: Build {plan.parent_assembly_id} with its declared drawers."""\n\n'
            "from dataclasses import replace\n"
            "from assemblies.specification import (\n"
            "    BuiltAssembly, BuiltChildAssembly, BuiltPurchasedHardware,\n"
            ")\n\n"
            "from .builder import BUILDER as CABINET_BUILDER\n"
            "from .drawer_installation import CHILD_ASSEMBLIES, PURCHASED_HARDWARE\n"
            f"{imports}\n\n\n"
            f"DRAWER_BUILDERS = ({builders},)\n\n\n"
            "class CabinetWithDrawersBuilder:\n"
            "    \"\"\"Compose the cabinet and its independently placed drawer children.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        cabinet = CABINET_BUILDER.build()\n"
            "        children = tuple(\n"
            "            BuiltChildAssembly(spec, builder.build())\n"
            "            for spec, builder in zip(CHILD_ASSEMBLIES, DRAWER_BUILDERS)\n"
            "        )\n"
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
            "            spec=spec, parts=cabinet.parts, joints=cabinet.joints,\n"
            "            cuts=cabinet.cuts,\n"
            "            child_assemblies=cabinet.child_assemblies + children,\n"
            "            purchased_hardware=cabinet.purchased_hardware + hardware,\n"
            "        )\n\n\n"
            "BUILDER = CabinetWithDrawersBuilder()\n"
        )

    def _builder_import(self, drawer_id: str) -> str:
        return (
            f"from .drawers.{drawer_id}.builder import BUILDER as "
            f"{self._builder_name(drawer_id)}"
        )

    def _builder_name(self, drawer_id: str) -> str:
        return f"{drawer_id.upper()}_BUILDER"


__all__ = ["HettichKa5332CabinetDrawersBuilderRenderer"]
