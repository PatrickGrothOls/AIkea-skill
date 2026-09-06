"""Scope: Compose placed cabinet and base taxonomies under one wardrobe root."""

from __future__ import annotations

from assembly_taxonomy import (
    BaseAssemblyTaxonomy,
    PartPlacementTaxonomy,
    ProjectAssemblyTaxonomy,
)
from wardrobe_assembly_taxonomy import (
    ChildAssemblyTaxonomy,
    WardrobeAssemblyTaxonomy,
)


class WardrobeTaxonomyResolver:
    """Save base-first and then left-to-right cabinet child frames."""

    _ASSEMBLY_ID = "wardrobe_01"

    def resolve(self, project: ProjectAssemblyTaxonomy) -> ProjectAssemblyTaxonomy:
        base = next(
            assembly
            for assembly in project.assemblies
            if isinstance(assembly, BaseAssemblyTaxonomy)
        )
        cabinets = tuple(
            assembly
            for assembly in project.assemblies
            if not isinstance(assembly, BaseAssemblyTaxonomy)
        )
        children = tuple(
            self._child(assembly, base.global_left_mm)
            for assembly in (base, *cabinets)
        )
        wardrobe = WardrobeAssemblyTaxonomy(
            assembly_id=self._ASSEMBLY_ID,
            purpose="fitted_wardrobe",
            global_left_mm=base.global_left_mm,
            global_right_mm=base.global_right_mm,
            width_mm=base.width_mm,
            child_assemblies=children,
        )
        return ProjectAssemblyTaxonomy(project.assemblies, wardrobe)

    def _child(self, assembly, project_left_mm: float) -> ChildAssemblyTaxonomy:
        return ChildAssemblyTaxonomy(
            assembly_id=assembly.assembly_id,
            purpose=assembly.purpose,
            local_to_parent=PartPlacementTaxonomy.from_plane(
                (assembly.global_left_mm - project_left_mm, 0.0, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
        )


__all__ = ["WardrobeTaxonomyResolver"]
