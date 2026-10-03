"""Scope: Render configured panel entry points and explicit cabinet shelf-grid requests."""


class ConfiguredPanelModuleRenderer:
    """Expose editable construction inputs and views of the complete result."""

    def assembly_builder(self, assembly_id, recipe="cabinet"):
        return (
            f'"""Scope: Construct the editable {assembly_id} recipe with shared tools."""\n\n'
            "from configured_unit_builder import ConfiguredUnitBuilder\n"
            "from .spec import SPEC\n\n\n"
            "# Unselected fittings remain declared unresolved joints in this preview.\n"
            f"BUILDER = ConfiguredUnitBuilder(SPEC, recipe={recipe!r})\n"
        )

    def part_builder(self, assembly_id, part_id):
        return (
            f'"""Scope: Expose the constructed {part_id} owned by {assembly_id}."""\n\n'
            "from ...builder import BUILDER as ASSEMBLY_BUILDER\n\n\n"
            "class ConstructedPartView:\n"
            '    """Read the finished part through the same complete construction path."""\n\n'
            "    def build(self):\n"
            "        return next(part for part in ASSEMBLY_BUILDER.build().parts\n"
            f"                    if part.spec.part_id == {part_id!r})\n\n\n"
            "BUILDER = ConstructedPartView()\n"
        )

    def machining(self, assembly):
        requests = "\n".join(
            f"        PartMachiningSpec({part.part_id + '_shelf_grid'!r}, {part.part_id!r}, 'system_32'),"
            for part in assembly.parts if part.role == "side_panel"
        )
        return f"    machining=(\n{requests}\n    ),\n"
