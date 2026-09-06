"""Scope: Apply the correct part-placement policy to each project assembly."""

from __future__ import annotations

from assembly_taxonomy import (
    BaseAssemblyTaxonomy,
    ProjectAssemblyTaxonomy,
)
from base_part_placement_resolver import BasePartPlacementResolver
from storage_part_placement_resolver import StoragePartPlacementResolver


class ProjectPartPlacementResolver:
    """Complete every assembly taxonomy before generated files are rendered."""

    def __init__(self) -> None:
        self.storage = StoragePartPlacementResolver()
        self.base = BasePartPlacementResolver()

    def resolve(self, project: ProjectAssemblyTaxonomy) -> ProjectAssemblyTaxonomy:
        assemblies = tuple(
            self.base.resolve(assembly)
            if isinstance(assembly, BaseAssemblyTaxonomy)
            else self.storage.resolve(assembly)
            for assembly in project.assemblies
        )
        return ProjectAssemblyTaxonomy(assemblies, project.wardrobe)


__all__ = ["ProjectPartPlacementResolver"]
