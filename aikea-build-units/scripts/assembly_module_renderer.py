"""Scope: Render generated builder and local part access modules."""

from __future__ import annotations

from assembly_taxonomy import BaseAssemblyTaxonomy, LocalAssemblyTaxonomy, PartTaxonomy


AssemblyTaxonomy = LocalAssemblyTaxonomy | BaseAssemblyTaxonomy


class AssemblyModuleRenderer:
    """Create importable entry points around one authoritative local spec."""

    def assembly_builder(self, assembly: AssemblyTaxonomy) -> str:
        imports = "\n".join(
            f"from .parts.{part.part_id}.builder import BUILDER as {self._constant(part.part_id)}_BUILDER"
            for part in assembly.parts
        )
        builders = "\n".join(
            f"                {self._constant(part.part_id)}_BUILDER.build(cuts.for_part({part.part_id!r})),"
            for part in assembly.parts
        )
        class_name = f"{self._class_name(assembly.assembly_id)}Builder"
        return (
            f'"""Scope: Build every local part owned by {assembly.assembly_id}."""\n\n'
            "from assemblies.specification import BuiltAssembly\n"
            "from assembly_joint_machining_builder import AssemblyJointMachiningBuilder\n\n"
            "from .joints.spec import JOINTS\n"
            f"{imports}\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}:\n"
            "    \"\"\"Build the unit's local parts and retain its physical joints.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        cuts = AssemblyJointMachiningBuilder().build(SPEC, JOINTS)\n"
            "        return BuiltAssembly(\n"
            "            spec=SPEC,\n"
            "            parts=(\n"
            f"{builders}\n"
            "            ),\n"
            "            joints=JOINTS,\n"
            "            cuts=cuts.all,\n"
            "        )\n\n\n"
            f"BUILDER = {class_name}()\n"
        )

    def part_spec(self, assembly_id: str, part: PartTaxonomy) -> str:
        return (
            f'"""Scope: Expose the finished {part.part_id} specification for {assembly_id}."""\n\n'
            "from ...spec import SPEC as ASSEMBLY_SPEC\n\n\n"
            f"SPEC = ASSEMBLY_SPEC.part({part.part_id!r})\n"
        )

    def part_builder(self, assembly_id: str, part: PartTaxonomy) -> str:
        class_name = f"{self._class_name(part.part_id)}Builder"
        return (
            f'"""Scope: Build the local {part.part_id} part for {assembly_id}."""\n\n'
            "from assemblies.specification import BuiltPart\n\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}:\n"
            f"    \"\"\"Construct the {part.role} in its local manufacturing frame.\"\"\"\n\n"
            "    def build(self, cuts=()) -> BuiltPart:\n"
            "        from sheet_part_builder import SheetPartBuilder\n\n"
            "        return BuiltPart(SPEC, SheetPartBuilder().build(SPEC, cuts))\n\n\n"
            f"BUILDER = {class_name}()\n"
        )

    def joints_spec(self, assembly_id: str) -> str:
        return (
            f'"""Scope: Expose every physical joint owned by {assembly_id}."""\n\n'
            "from ..spec import SPEC as ASSEMBLY_SPEC\n\n\n"
            "JOINTS = ASSEMBLY_SPEC.joints\n"
        )

    def metadata_assembly_builder(self, assembly: AssemblyTaxonomy) -> str:
        imports = "\n".join(
            f"from .parts.{part.part_id}.builder import BUILDER as {self._constant(part.part_id)}_BUILDER"
            for part in assembly.parts
        )
        builders = "\n".join(
            f"                {self._constant(part.part_id)}_BUILDER.build(),"
            for part in assembly.parts
        )
        class_name = f"{self._class_name(assembly.assembly_id)}Builder"
        return (
            f'"""Scope: Build the resolved part plan for {assembly.assembly_id}."""\n\n'
            "from assemblies.specification import AssemblyBuildPlan\n\n"
            "from .joints.spec import JOINTS\n"
            f"{imports}\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}:\n"
            "    \"\"\"Combine the unit's local part plans and physical joints.\"\"\"\n\n"
            "    def build(self) -> AssemblyBuildPlan:\n"
            "        return AssemblyBuildPlan(\n"
            "            assembly_spec=SPEC,\n"
            "            parts=(\n"
            f"{builders}\n"
            "            ),\n"
            "            joints=JOINTS,\n"
            "        )\n\n\n"
            f"BUILDER = {class_name}()\n"
        )

    def metadata_part_builder(self, assembly_id: str, part: PartTaxonomy) -> str:
        class_name = f"{self._class_name(part.part_id)}Builder"
        return (
            f'"""Scope: Build the resolved {part.part_id} plan for {assembly_id}."""\n\n'
            "from assemblies.specification import PartBuildPlan\n\n"
            "from .spec import SPEC\n\n\n"
            f"class {class_name}:\n"
            f"    \"\"\"Provide the build plan for the {part.role}.\"\"\"\n\n"
            "    def build(self) -> PartBuildPlan:\n"
            "        return PartBuildPlan(SPEC)\n\n\n"
            f"BUILDER = {class_name}()\n"
        )

    def package(self, responsibility: str) -> str:
        return f'"""Scope: {responsibility}."""\n'

    def _class_name(self, value: str) -> str:
        return "".join(part.capitalize() for part in value.split("_"))

    def _constant(self, value: str) -> str:
        return value.upper()
