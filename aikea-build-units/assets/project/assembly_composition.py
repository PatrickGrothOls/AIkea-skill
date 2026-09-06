"""Scope: Define declared and built values for nested assemblies and hardware."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, TYPE_CHECKING

from .assembly_placement import LocalToParentPlacement

if TYPE_CHECKING:
    from .specification import PartSpec


class AssemblyCompositionError(ValueError):
    """Report a built item that differs from its owning assembly specification."""


@dataclass(frozen=True)
class ChildAssemblySpec:
    """Declare one child assembly and its frame inside its parent."""

    assembly_id: str
    purpose: str
    local_to_parent: LocalToParentPlacement


@dataclass(frozen=True)
class PurchasedHardwareSpec:
    """Declare one purchased instance through a registered hardware asset."""

    hardware_id: str
    manufacturer: str
    product_code: str
    hardware_asset_id: str
    local_to_parent: LocalToParentPlacement | None
    geometry_selector: str | None = None


class AssemblySpecification(Protocol):
    """Describe the shared identity and composition fields of any assembly."""

    assembly_id: str
    purpose: str
    parts: tuple[PartSpec, ...]
    child_assemblies: tuple[ChildAssemblySpec, ...]
    purchased_hardware: tuple[PurchasedHardwareSpec, ...]


@dataclass(frozen=True)
class BuiltPurchasedHardware:
    """Retain optional verified geometry with its declared instance."""

    spec: PurchasedHardwareSpec
    solid: Any | None

    @property
    def has_geometry(self) -> bool:
        return self.solid is not None


@dataclass(frozen=True)
class BuiltChildAssembly:
    """Retain one built child with its declared parent placement."""

    spec: ChildAssemblySpec
    assembly: BuiltAssembly

    def __post_init__(self) -> None:
        expected_identity = self.spec.assembly_id, self.spec.purpose
        built_identity = self.assembly.spec.assembly_id, self.assembly.spec.purpose
        if built_identity != expected_identity:
            raise AssemblyCompositionError(
                "built child identity does not match its declared child specification"
            )


@dataclass(frozen=True)
class BuiltPart:
    """Retain one manufactured solid with its declared assembly placement."""

    spec: PartSpec
    solid: Any


@dataclass(frozen=True)
class BuiltAssembly:
    """Retain one complete materialized assembly and enforce its declaration."""

    spec: AssemblySpecification
    parts: tuple[BuiltPart, ...]
    joints: tuple[Any, ...]
    cuts: tuple[Any, ...] = ()
    child_assemblies: tuple[BuiltChildAssembly, ...] = ()
    purchased_hardware: tuple[BuiltPurchasedHardware, ...] = ()

    def __post_init__(self) -> None:
        built_part_specs = tuple(part.spec for part in self.parts)
        if built_part_specs != self.spec.parts:
            raise AssemblyCompositionError(
                "built parts do not match their declared specifications"
            )
        built_child_specs = tuple(child.spec for child in self.child_assemblies)
        if built_child_specs != self.spec.child_assemblies:
            raise AssemblyCompositionError(
                "built child assemblies do not match their declared placements"
            )
        built_hardware_specs = tuple(item.spec for item in self.purchased_hardware)
        if built_hardware_specs != self.spec.purchased_hardware:
            raise AssemblyCompositionError(
                "built purchased hardware does not match its declared placements"
            )
