"""Scope: Declare an ordered wardrobe root and its positioned children."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from assembly_taxonomy import PartPlacementTaxonomy


@dataclass(frozen=True)
class ChildAssemblyTaxonomy:
    """Declare one child assembly and its frame inside a composed parent."""

    assembly_id: str
    purpose: str
    local_to_parent: PartPlacementTaxonomy


@dataclass(frozen=True)
class WardrobeAssemblyTaxonomy:
    """Own the ordered physical assemblies in one fitted wardrobe."""

    assembly_id: str
    purpose: str
    global_left_mm: float
    global_right_mm: float
    width_mm: float
    child_assemblies: tuple[ChildAssemblyTaxonomy, ...]


__all__ = ["ChildAssemblyTaxonomy", "WardrobeAssemblyTaxonomy"]
