"""Scope: Define reusable hardware component and installed-purchase identities."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ConnectionPurchaseSpec:
    """Link one installed purchase to a connection occurrence in its owner frame."""

    joint_id: str
    connector_index: int
    component: str


@dataclass(frozen=True)
class HardwarePurchaseSpec:
    """Map a modeled member to one installed unit in a relative owner frame."""

    purchase_id: str
    product_code: str
    unit: str
    member: str
    required_members: tuple[str, ...]
    owner_levels_up: int = 0
    mounting_fasteners_included: bool = True
    connection: ConnectionPurchaseSpec | None = None


@dataclass(frozen=True)
class PurchasedHardwareSpec:
    """Retain placement and purchase evidence independently of CAD solid count."""

    hardware_id: str
    manufacturer: str
    product_code: str
    hardware_asset_id: str
    local_to_parent: Any | None
    geometry_selector: str | None = None
    purchase: HardwarePurchaseSpec | None = None
    mounting_part_id: str | None = None
