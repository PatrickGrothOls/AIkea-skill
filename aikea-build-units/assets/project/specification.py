"""Scope: Define immutable values shared by generated local assembly files."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BoundaryPoint:
    x_mm: float
    height_mm: float


@dataclass(frozen=True)
class PartSpec:
    part_id: str
    role: str
    dimensions_mm: tuple[tuple[str, float], ...]
    outline_mm: tuple[BoundaryPoint, ...] = ()
    local_size_mm: tuple[float, float, float] = ()
    inside_face: str = ""


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
    parts: tuple[PartSpec, ...]
    joints: tuple[JointSpec | CabineoJointSpec, ...]

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)


@dataclass(frozen=True)
class BuiltPart:
    spec: PartSpec
    solid: Any


@dataclass(frozen=True)
class BuiltAssembly:
    spec: AssemblySpec
    parts: tuple[BuiltPart, ...]
    joints: tuple[JointSpec | CabineoJointSpec, ...]
    cuts: tuple[Any, ...] = ()
