"""Scope: Transfer confirmed project stock choices to standard recipe parts."""

from dataclasses import replace

from assembly_taxonomy import ProjectAssemblyTaxonomy
from design_decisions import DesignDecision


class PartMaterialResolver:
    """Use the saved stock description verbatim; thickness remains on the part."""

    GROUPS = {
        "door_panel": "door_front_material",
        "back_panel": "back_panel_material",
    }

    def resolve(
        self, taxonomy: ProjectAssemblyTaxonomy, decisions: tuple[DesignDecision, ...]
    ) -> ProjectAssemblyTaxonomy:
        # The global input reader has already required one decision per group.
        selected = {choice.subject: choice.decision for choice in decisions}
        return replace(taxonomy, assemblies=tuple(
            replace(assembly, parts=tuple(
                replace(part, material_id=part.material_id or selected[
                    self.GROUPS.get(part.role, "cabinet_carcass_material")
                ])
                for part in assembly.parts
            ))
            for assembly in taxonomy.assemblies
        ))
