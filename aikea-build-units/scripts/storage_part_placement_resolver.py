"""Scope: Resolve every storage-cabinet part frame from its local taxonomy."""

from __future__ import annotations

from dataclasses import replace
from math import hypot

from assembly_taxonomy import (
    AssemblyTaxonomyInputError,
    LocalAssemblyTaxonomy,
    PartPlacementTaxonomy,
    PartTaxonomy,
)


class StoragePartPlacementResolver:
    """Make one cabinet specification authoritative for all part positions."""

    def __init__(self) -> None:
        self._part_resolvers = {
            "left_side": self._left_side,
            "right_side": self._right_side,
            "back_panel": self._back_panel,
            "door_panel": self._door_panel,
        }
        self._role_resolvers = {
            "shelf_panel": self._shelf_panel,
            "top_panel": self._top_panel,
        }

    def resolve(self, assembly: LocalAssemblyTaxonomy) -> LocalAssemblyTaxonomy:
        parts = tuple(
            replace(part, local_to_parent=self._resolve_part(part, assembly))
            for part in assembly.parts
        )
        return replace(assembly, parts=parts)

    def _resolve_part(
        self,
        part: PartTaxonomy,
        assembly: LocalAssemblyTaxonomy,
    ) -> PartPlacementTaxonomy:
        resolver = self._part_resolvers.get(part.part_id)
        resolver = resolver or self._role_resolvers.get(part.role)
        if resolver is None:
            raise AssemblyTaxonomyInputError(
                [f"no assembly placement exists for {part.part_id}"]
            )
        return resolver(part, assembly)

    def _left_side(self, _part, assembly) -> PartPlacementTaxonomy:
        return self._placement(
            (0.0, 0.0, assembly.base_height_mm),
            (0.0, 1.0, 0.0),
            (1.0, 0.0, 0.0),
        )

    def _right_side(self, _part, assembly) -> PartPlacementTaxonomy:
        return self._placement(
            (assembly.width_mm, assembly.inside_depth_mm, assembly.base_height_mm),
            (0.0, -1.0, 0.0),
            (-1.0, 0.0, 0.0),
        )

    def _back_panel(self, _part, assembly) -> PartPlacementTaxonomy:
        return self._placement(
            (0.0, assembly.depth_mm, assembly.base_height_mm),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        )

    def _door_panel(self, _part, assembly) -> PartPlacementTaxonomy:
        left_gap_mm = (assembly.width_mm - assembly.door_width_mm) / 2.0
        return self._placement(
            (left_gap_mm, 0.0, assembly.door_bottom_mm),
            (1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
        )

    def _shelf_panel(self, part, assembly) -> PartPlacementTaxonomy:
        dimensions = self._dimensions(part)
        return self._placement(
            (
                dimensions["assembly_x"],
                dimensions["assembly_y"],
                assembly.base_height_mm + dimensions["bottom_height"],
            ),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

    def _top_panel(self, part, assembly) -> PartPlacementTaxonomy:
        dimensions = self._dimensions(part)
        run_mm = dimensions["end_x"] - dimensions["start_x"]
        rise_mm = dimensions["end_height"] - dimensions["start_height"]
        length_mm = hypot(run_mm, rise_mm)
        tangent = (run_mm / length_mm, 0.0, rise_mm / length_mm)
        outside_normal = (-rise_mm / length_mm, 0.0, run_mm / length_mm)
        outside_start = (
            dimensions["start_x"],
            0.0,
            assembly.base_height_mm + dimensions["start_height"],
        )
        inside_start = tuple(
            coordinate - normal * dimensions["thickness"]
            for coordinate, normal in zip(outside_start, outside_normal)
        )
        return self._placement(inside_start, tangent, outside_normal)

    def _placement(self, origin, local_x, local_z) -> PartPlacementTaxonomy:
        return PartPlacementTaxonomy.from_plane(origin, local_x, local_z)

    def _dimensions(self, part: PartTaxonomy) -> dict[str, float]:
        return {name: float(value) for name, value in part.dimensions_mm}


__all__ = ["StoragePartPlacementResolver"]
