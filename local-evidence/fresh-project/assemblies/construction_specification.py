"""Scope: Describe explicit panel construction independently of furniture recipes."""

from dataclasses import dataclass
from typing import Any, Protocol

from .specification import (
    AssemblySpecification, ChildAssemblySpec, PartMachiningSpec, PartSpec, PurchasedHardwareSpec, SurfaceDrillingSpec, SurfaceGrooveSpec, SurfacePocketSpec,
)
from .construction_requirement import ConstructionRequirementSpec


class ConstructionSpecification(AssemblySpecification, Protocol):
    """Accept both configured metadata and directly authored construction."""

    joints: tuple[Any, ...]
    machining: tuple[PartMachiningSpec | SurfaceDrillingSpec | SurfaceGrooveSpec | SurfacePocketSpec, ...]

    def part(self, part_id: str) -> PartSpec: ...


@dataclass(frozen=True)
class PanelAssemblySpec:
    """Hold editable construction inputs from a configurator or authored layout."""

    assembly_id: str
    purpose: str
    parts: tuple[PartSpec, ...] = ()
    joints: tuple[Any, ...] = ()
    child_assemblies: tuple[ChildAssemblySpec, ...] = ()
    purchased_hardware: tuple[PurchasedHardwareSpec, ...] = ()
    machining: tuple[PartMachiningSpec | SurfaceDrillingSpec | SurfaceGrooveSpec | SurfacePocketSpec, ...] = ()
    requirements: tuple[ConstructionRequirementSpec, ...] | None = None

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)
