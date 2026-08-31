"""Scope: Render one generated wardrobe-root specification and builder."""

from __future__ import annotations

from pathlib import Path

from wardrobe_assembly_taxonomy import (
    ChildAssemblyTaxonomy,
    WardrobeAssemblyTaxonomy,
)


class WardrobeAssemblyRenderer:
    """Make the saved child order executable without feature-specific logic."""

    def render(self, wardrobe: WardrobeAssemblyTaxonomy) -> dict[Path, str]:
        root = Path("assemblies") / wardrobe.assembly_id
        return {
            root / "__init__.py": (
                f'"""Scope: Contain the {wardrobe.assembly_id} root assembly."""\n'
            ),
            root / "spec.py": self._spec(wardrobe),
            root / "builder.py": self._builder(wardrobe),
            root / "complete_builder.py": (
                f'"""Scope: Expose the complete {wardrobe.assembly_id} builder."""\n\n'
                "from .builder import BUILDER\n"
            ),
        }

    def _spec(self, wardrobe: WardrobeAssemblyTaxonomy) -> str:
        children = "\n".join(
            self._child_spec(child) for child in wardrobe.child_assemblies
        )
        return (
            f'"""Scope: Own the ordered children of {wardrobe.assembly_id}."""\n\n'
            "from assemblies.specification import (\n"
            "    AxisBasis, AxisDirection, ChildAssemblySpec, CompositeAssemblySpec,\n"
            "    LocalToParentPlacement, Point3D,\n"
            ")\n\n\n"
            "SPEC = CompositeAssemblySpec(\n"
            f"    assembly_id={wardrobe.assembly_id!r},\n"
            f"    purpose={wardrobe.purpose!r},\n"
            "    child_assemblies=(\n"
            f"{children}\n"
            "    ),\n"
            ")\n"
        )

    def _child_spec(self, child: ChildAssemblyTaxonomy) -> str:
        placement = child.local_to_parent
        origin = placement.origin_in_parent_mm
        return (
            "        ChildAssemblySpec(\n"
            f"            assembly_id={child.assembly_id!r},\n"
            f"            purpose={child.purpose!r},\n"
            "            local_to_parent=LocalToParentPlacement(\n"
            f"                Point3D{origin!r},\n"
            "                AxisBasis(\n"
            f"                    AxisDirection{placement.local_x_in_parent!r},\n"
            f"                    AxisDirection{placement.local_y_in_parent!r},\n"
            f"                    AxisDirection{placement.local_z_in_parent!r},\n"
            "                ),\n"
            "            ),\n"
            "        ),"
        )

    def _builder(self, wardrobe: WardrobeAssemblyTaxonomy) -> str:
        imports = "\n".join(
            f"from ..{child.assembly_id}.complete_builder import BUILDER as "
            f"{child.assembly_id.upper()}_BUILDER"
            for child in wardrobe.child_assemblies
        )
        builders = ", ".join(
            f"{child.assembly_id.upper()}_BUILDER"
            for child in wardrobe.child_assemblies
        )
        return (
            f'"""Scope: Build every ordered child of {wardrobe.assembly_id}."""\n\n'
            "from assemblies.specification import BuiltAssembly, BuiltChildAssembly\n\n"
            f"{imports}\n"
            "from .spec import SPEC\n\n\n"
            f"CHILD_BUILDERS = ({builders},)\n\n\n"
            "class WardrobeBuilder:\n"
            "    \"\"\"Build the base and every complete cabinet in saved order.\"\"\"\n\n"
            "    def build(self) -> BuiltAssembly:\n"
            "        children = tuple(\n"
            "            BuiltChildAssembly(spec, builder.build())\n"
            "            for spec, builder in zip(\n"
            "                SPEC.child_assemblies, CHILD_BUILDERS, strict=True\n"
            "            )\n"
            "        )\n"
            "        return BuiltAssembly(SPEC, (), (), child_assemblies=children)\n\n\n"
            "BUILDER = WardrobeBuilder()\n"
        )


__all__ = ["WardrobeAssemblyRenderer"]
