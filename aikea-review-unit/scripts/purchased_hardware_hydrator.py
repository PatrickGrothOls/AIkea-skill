"""Scope: Fill declared purchased-hardware instances with exact local geometry."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Protocol


class HardwareGeometryResolver(Protocol):
    """Resolve one declared asset without deciding its placement."""

    def resolve(self, project_root: Path, spec: Any) -> Any: ...


class PurchasedHardwareHydrator:
    """Hydrate every unresolved hardware instance at arbitrary assembly depth."""

    def __init__(self, geometry: HardwareGeometryResolver) -> None:
        self.geometry = geometry

    def hydrate(self, project_root: Path, assembly: Any) -> Any:
        hardware = tuple(
            item
            if item.has_geometry
            else replace(item, solid=self.geometry.resolve(project_root, item.spec))
            for item in assembly.purchased_hardware
        )
        children = tuple(
            replace(
                child,
                assembly=self.hydrate(project_root, child.assembly),
            )
            for child in assembly.child_assemblies
        )
        return replace(
            assembly,
            child_assemblies=children,
            purchased_hardware=hardware,
        )


__all__ = ["HardwareGeometryResolver", "PurchasedHardwareHydrator"]
