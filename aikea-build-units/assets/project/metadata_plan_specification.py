"""Scope: Define immutable values shared by generated local assembly files."""

from __future__ import annotations

from dataclasses import dataclass


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


@dataclass(frozen=True)
class JointSpec:
    joint_id: str
    participant_ids: tuple[str, ...]
    purpose: str


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
    joints: tuple[JointSpec, ...]

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
    modules: tuple[BaseModuleSpec, ...]
    parts: tuple[PartSpec, ...]
    joints: tuple[JointSpec, ...]

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)


@dataclass(frozen=True)
class PartBuildPlan:
    spec: PartSpec


@dataclass(frozen=True)
class AssemblyBuildPlan:
    assembly_spec: AssemblySpec | BaseAssemblySpec
    parts: tuple[PartBuildPlan, ...]
    joints: tuple[JointSpec, ...]
