"""Scope: Define declared and built values for nested assemblies and hardware."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, TYPE_CHECKING

from .assembly_placement import LocalToParentPlacement

if TYPE_CHECKING:
    from .specification import BuiltAssembly


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
    """Declare one purchased hardware instance and its vendor-CAD placement."""

    hardware_id: str
    manufacturer: str
    product_code: str
    cad_asset_path: str
    local_to_parent: LocalToParentPlacement


class AssemblySpecification(Protocol):
    """Describe the shared identity and composition fields of any assembly."""

    assembly_id: str
    purpose: str
    child_assemblies: tuple[ChildAssemblySpec, ...]
    purchased_hardware: tuple[PurchasedHardwareSpec, ...]


@dataclass(frozen=True)
class BuiltPurchasedHardware:
    """Retain imported hardware geometry with its declared instance."""

    spec: PurchasedHardwareSpec
    solid: Any


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
