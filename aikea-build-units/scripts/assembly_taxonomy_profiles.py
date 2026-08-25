"""Scope: Resolve a unit purpose to its versioned construction taxonomy owner."""

from __future__ import annotations

from typing import Protocol

from assembly_taxonomy import BoundaryPoint, JointTaxonomy, PartTaxonomy
from tall_storage_taxonomy import TallStorageTaxonomy


class AssemblyTaxonomyProfile(Protocol):
    """Define the part and joint taxonomy operations required by the resolver."""

    def build_parts(
        self,
        top: tuple[BoundaryPoint, ...],
        width_mm: float,
        depth_mm: float,
        door_width_mm: float,
        base_height_mm: float,
        panel_thickness_mm: float,
        door_thickness_mm: float,
        back_thickness_mm: float,
    ) -> tuple[PartTaxonomy, ...]: ...

    def build_joints(self, top_panel_count: int) -> tuple[JointTaxonomy, ...]: ...


class AssemblyTaxonomyProfileRegistry:
    """Keep supported construction purposes separate from boundary calculation."""

    def __init__(self) -> None:
        self._profiles: dict[str, AssemblyTaxonomyProfile] = {
            "tall_storage": TallStorageTaxonomy(),
        }

    def get(self, purpose: str) -> AssemblyTaxonomyProfile | None:
        return self._profiles.get(purpose)
