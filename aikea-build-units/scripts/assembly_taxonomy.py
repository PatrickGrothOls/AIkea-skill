"""Scope: Define resolved local assembly, part, and joint taxonomy values."""

from __future__ import annotations

from dataclasses import dataclass

from wardrobe_assembly_taxonomy import WardrobeAssemblyTaxonomy


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
class PartPlacementTaxonomy:
    """Describe one manufactured part's rigid frame inside its assembly."""

    origin_in_parent_mm: tuple[float, float, float]
    local_x_in_parent: tuple[float, float, float]
    local_y_in_parent: tuple[float, float, float]
    local_z_in_parent: tuple[float, float, float]

    @classmethod
    def from_plane(
        cls,
        origin_in_parent_mm: tuple[float, float, float],
        local_x_in_parent: tuple[float, float, float],
        local_z_in_parent: tuple[float, float, float],
    ) -> "PartPlacementTaxonomy":
        x_x, x_y, x_z = local_x_in_parent
        z_x, z_y, z_z = local_z_in_parent
        local_y_in_parent = (
            (z_y * x_z) - (z_z * x_y),
            (z_z * x_x) - (z_x * x_z),
            (z_x * x_y) - (z_y * x_x),
        )
        return cls(
            origin_in_parent_mm,
            local_x_in_parent,
            local_y_in_parent,
            local_z_in_parent,
        )


@dataclass(frozen=True)
class PartTaxonomy:
    part_id: str
    role: str
    dimensions_mm: tuple[tuple[str, float], ...]
    outline_mm: tuple[BoundaryPoint, ...] = ()
    local_size_mm: tuple[float, float, float] = ()
    inside_face: str = ""
    local_to_parent: PartPlacementTaxonomy | None = None


@dataclass(frozen=True)
class JointTaxonomy:
    joint_id: str
    participant_ids: tuple[str, ...]
    purpose: str
    joint_type: str = "unresolved"


@dataclass(frozen=True)
class CabineoJointTaxonomy:
    joint_id: str
    source_part_id: str
    target_part_id: str
    source_face: str
    source_edge: str
    connector_layout: str
    purpose: str = "structural_seam"
    joint_type: str = "cabineo"

    @property
    def participant_ids(self) -> tuple[str, str]:
        return self.source_part_id, self.target_part_id


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
    door_bottom: str
    door_bottom_mm: float
    parts: tuple[PartTaxonomy, ...]
    joints: tuple[JointTaxonomy | CabineoJointTaxonomy, ...]


@dataclass(frozen=True)
class BaseModuleTaxonomy:
    module_id: str
    start_x_mm: float
    end_x_mm: float

    @property
    def width_mm(self) -> float:
        return self.end_x_mm - self.start_x_mm


@dataclass(frozen=True)
class BaseAssemblyTaxonomy:
    assembly_id: str
    purpose: str
    global_left_mm: float
    global_right_mm: float
    width_mm: float
    depth_mm: float
    height_mm: float
    plinth_front: str
    plinth_recess_mm: float
    modules: tuple[BaseModuleTaxonomy, ...]
    parts: tuple[PartTaxonomy, ...]
    joints: tuple[JointTaxonomy | CabineoJointTaxonomy, ...]


@dataclass(frozen=True)
class ProjectAssemblyTaxonomy:
    assemblies: tuple[LocalAssemblyTaxonomy | BaseAssemblyTaxonomy, ...]
    wardrobe: WardrobeAssemblyTaxonomy | None = None
