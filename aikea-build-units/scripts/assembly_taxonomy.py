"""Scope: Define resolved local assembly, part, and joint taxonomy values."""

from __future__ import annotations

from dataclasses import dataclass


class AssemblyTaxonomyInputError(ValueError):
    """Report project values that cannot produce a local taxonomy."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = tuple(problems)
        super().__init__("; ".join(problems))


@dataclass(frozen=True)
class BoundaryPoint:
    x_mm: float
    height_mm: float


@dataclass(frozen=True)
class PartTaxonomy:
    part_id: str
    role: str
    dimensions_mm: tuple[tuple[str, float], ...]
    outline_mm: tuple[BoundaryPoint, ...] = ()


@dataclass(frozen=True)
class JointTaxonomy:
    joint_id: str
    participant_ids: tuple[str, ...]
    purpose: str


@dataclass(frozen=True)
class LocalAssemblyTaxonomy:
    assembly_id: str
    purpose: str
    global_left_mm: float
    global_right_mm: float
    width_mm: float
    top: tuple[BoundaryPoint, ...]
    depth_mm: float
    inside_depth_mm: float
    door_width_mm: float
    base_height_mm: float
    parts: tuple[PartTaxonomy, ...]
    joints: tuple[JointTaxonomy, ...]


@dataclass(frozen=True)
class ProjectAssemblyTaxonomy:
    assemblies: tuple[LocalAssemblyTaxonomy, ...]
