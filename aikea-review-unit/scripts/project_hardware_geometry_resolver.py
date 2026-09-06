"""Scope: Route declared hardware assets to exact project-local CAD providers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class ProjectHardwareGeometryError(ValueError):
    """Report a declared hardware asset without an exact geometry provider."""


class ProjectHardwareGeometryProvider(Protocol):
    """Load one supported asset from the project's local hardware library."""

    def supports(self, asset_id: str) -> bool: ...

    def resolve(self, project_root: Path, spec: Any) -> Any: ...


class ProjectHardwareGeometryResolver:
    """Use a small provider registry without feature checks in tree traversal."""

    def __init__(
        self,
        providers: tuple[ProjectHardwareGeometryProvider, ...] | None = None,
    ) -> None:
        self.providers = (
            providers if providers is not None else self._default_providers()
        )

    def resolve(self, project_root: Path, spec: Any) -> Any:
        provider = next(
            (
                item
                for item in self.providers
                if item.supports(spec.hardware_asset_id)
            ),
            None,
        )
        if provider is None:
            raise ProjectHardwareGeometryError(
                f"no exact geometry provider for {spec.hardware_asset_id}"
            )
        return provider.resolve(project_root, spec)

    def _default_providers(self) -> tuple[ProjectHardwareGeometryProvider, ...]:
        from blum_movento_geometry_provider import BlumMoventoGeometryProvider
        from hettich_ka_4532_spacer_geometry_provider import (
            HettichKa4532SpacerGeometryProvider,
        )
        from hettich_ka_5332_geometry_provider import HettichKa5332GeometryProvider
        from riex_nc70_geometry_provider import RiexNc70GeometryProvider

        return (
            BlumMoventoGeometryProvider(),
            HettichKa4532SpacerGeometryProvider(),
            HettichKa5332GeometryProvider(),
            RiexNc70GeometryProvider(),
        )


__all__ = [
    "ProjectHardwareGeometryError",
    "ProjectHardwareGeometryProvider",
    "ProjectHardwareGeometryResolver",
]
