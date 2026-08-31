"""Scope: Resolve every structural-base part frame from its local taxonomy."""

from __future__ import annotations

from dataclasses import replace

from assembly_taxonomy import (
    AssemblyTaxonomyInputError,
    BaseAssemblyTaxonomy,
    PartPlacementTaxonomy,
    PartTaxonomy,
)


class BasePartPlacementResolver:
    """Make one base specification authoritative for all part positions."""

    def __init__(self) -> None:
        self._role_resolvers = {
            "base_deck": self._deck,
            "base_rail": self._rail,
            "base_brace": self._brace,
        }

    def resolve(self, assembly: BaseAssemblyTaxonomy) -> BaseAssemblyTaxonomy:
        parts = tuple(
            replace(part, local_to_parent=self._resolve_part(part, assembly))
            for part in assembly.parts
        )
        return replace(assembly, parts=parts)

    def _resolve_part(
        self,
        part: PartTaxonomy,
        assembly: BaseAssemblyTaxonomy,
    ) -> PartPlacementTaxonomy:
        resolver = self._role_resolvers.get(part.role)
        if resolver is None:
            raise AssemblyTaxonomyInputError(
                [f"no base placement exists for {part.part_id}"]
            )
        return resolver(part, assembly)

    def _deck(self, part, assembly) -> PartPlacementTaxonomy:
        module = self._module(part, assembly)
        dimensions = self._dimensions(part)
        return self._placement(
            (
                module.start_x_mm,
                0.0,
                assembly.height_mm - dimensions["thickness"],
            ),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

    def _rail(self, part, assembly) -> PartPlacementTaxonomy:
        module = self._module(part, assembly)
        dimensions = self._dimensions(part)
        origin_y_mm = assembly.plinth_recess_mm + dimensions["thickness"]
        if part.part_id.startswith("back_rail_"):
            origin_y_mm = assembly.depth_mm
        return self._placement(
            (module.start_x_mm, origin_y_mm, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        )

    def _brace(self, part, assembly) -> PartPlacementTaxonomy:
        module = self._module(part, assembly)
        dimensions = self._dimensions(part)
        front_rail = next(
            item
            for item in assembly.parts
            if item.part_id == f"front_rail_{self._module_suffix(part)}"
        )
        front_thickness_mm = self._dimensions(front_rail)["thickness"]
        front_inside_y_mm = assembly.plinth_recess_mm + front_thickness_mm
        start_x_mm = (
            module.start_x_mm
            + dimensions["center_x"]
            - (dimensions["thickness"] / 2.0)
        )
        return self._placement(
            (start_x_mm, front_inside_y_mm, 0.0),
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
        )

    def _module(self, part: PartTaxonomy, assembly: BaseAssemblyTaxonomy):
        module_id = f"base_module_{self._module_suffix(part)}"
        return next(module for module in assembly.modules if module.module_id == module_id)

    def _module_suffix(self, part: PartTaxonomy) -> str:
        fields = part.part_id.split("_")
        return fields[-2] if part.role == "base_brace" else fields[-1]

    def _placement(self, origin, local_x, local_z) -> PartPlacementTaxonomy:
        return PartPlacementTaxonomy.from_plane(origin, local_x, local_z)

    def _dimensions(self, part: PartTaxonomy) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["BasePartPlacementResolver"]
