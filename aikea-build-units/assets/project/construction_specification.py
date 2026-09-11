"""Scope: Describe explicit panel construction independently of furniture recipes."""

from dataclasses import dataclass
from typing import Any

from .specification import ChildAssemblySpec, PartSpec, PurchasedHardwareSpec


@dataclass(frozen=True)
class PartMachiningSpec:
    """Request a supported local operation without relying on a part's role."""

    machining_id: str
    part_id: str
    operation_type: str


@dataclass(frozen=True)
class PanelAssemblySpec:
    """Hold editable construction inputs from a configurator or authored layout."""

    assembly_id: str
    purpose: str
    parts: tuple[PartSpec, ...] = ()
    joints: tuple[Any, ...] = ()
    child_assemblies: tuple[ChildAssemblySpec, ...] = ()
    purchased_hardware: tuple[PurchasedHardwareSpec, ...] = ()
    machining: tuple[PartMachiningSpec, ...] = ()

    def part(self, part_id: str) -> PartSpec:
        return next(part for part in self.parts if part.part_id == part_id)
