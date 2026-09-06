"""Scope: Define immutable values shared by generated local assembly files."""

from __future__ import annotations

from dataclasses import dataclass
from .assembly_composition import (
    AssemblyCompositionError,
    AssemblySpecification,
    BuiltAssembly,
    BuiltChildAssembly,
    BuiltPart,
    BuiltPurchasedHardware,
    ChildAssemblySpec,
    PurchasedHardwareSpec,
)
from .assembly_placement import (
    AxisBasis,
    AxisDirection,
    AssemblyPlacementError,
    IDENTITY_AXIS_BASIS,
    IDENTITY_LOCAL_TO_PARENT,
    LocalToParentPlacement,
    Point3D,
)


@dataclass(frozen=True)
class BoundaryPoint:
    x_mm: float
    height_mm: float


@dataclass(frozen=True)
class PartSpec:
    part_id: str
    role: str
    dimensions_mm: tuple[tuple[str, float], ...]
    local_to_parent: LocalToParentPlacement
    outline_mm: tuple[BoundaryPoint, ...] = ()
    local_size_mm: tuple[float, float, float] = ()
    inside_face: str = ""


@dataclass(frozen=True)
class CompositeAssemblySpec:
    """Declare a physical parent whose contents are nested assemblies."""

    assembly_id: str
    purpose: str
    child_assemblies: tuple[ChildAssemblySpec, ...]
    parts: tuple[PartSpec, ...] = ()
    purchased_hardware: tuple[PurchasedHardwareSpec, ...] = ()


@dataclass(frozen=True)
class JointSpec:
    joint_id: str
    participant_ids: tuple[str, ...]
    purpose: str
    joint_type: str = "unresolved"


@dataclass(frozen=True)
class CabineoJointSpec:
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
class AssemblySpec:
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
    parts: tuple[PartSpec, ...]
    joints: tuple[JointSpec | CabineoJointSpec, ...]
    child_assemblies: tuple[ChildAssemblySpec, ...] = ()
    purchased_hardware: tuple[PurchasedHardwareSpec, ...] = ()

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)


@dataclass(frozen=True)
class BaseModuleSpec:
    module_id: str
    start_x_mm: float
    end_x_mm: float


@dataclass(frozen=True)
class BaseAssemblySpec:
    assembly_id: str
    purpose: str
    global_left_mm: float
    global_right_mm: float
    width_mm: float
    depth_mm: float
    height_mm: float
    plinth_front: str
    plinth_recess_mm: float
    modules: tuple[BaseModuleSpec, ...]
    parts: tuple[PartSpec, ...]
    joints: tuple[JointSpec | CabineoJointSpec, ...]
    child_assemblies: tuple[ChildAssemblySpec, ...] = ()
    purchased_hardware: tuple[PurchasedHardwareSpec, ...] = ()

    @property
    def base_height_mm(self) -> float:
        return self.height_mm

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)
