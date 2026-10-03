"""Scope: Load exact registered Riex NC70 components from project storage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from riex_nc70_hardware_loader import RiexNc70HardwareLoader


class RiexNc70GeometryProvider:
    """Verify the source set once and select geometry by registered asset id."""

    _ASSETS = {
        "riex-nc70-f000001-closed": "closed_hinge",
        "riex-nc70-f000001-open": "open_hinge",
        "riex-nc70-f000049-h0-euroscrew-plate": "mounting_plate",
    }

    def __init__(self) -> None:
        self.loader = RiexNc70HardwareLoader()
        self.cache: dict[Path, Any] = {}

    def supports(self, asset_id: str) -> bool:
        return asset_id in self._ASSETS

    def resolve(self, project_root: Path, spec: Any) -> Any:
        root = project_root.resolve()
        if root not in self.cache:
            hardware_root = project_root / "hardware/riex/nc70"
            self.cache[root] = self.loader.load(hardware_root)
        shape = getattr(
            self.cache[root],
            self._ASSETS[spec.hardware_asset_id],
        )
        return self._workplane(shape)

    def _workplane(self, shape: Any) -> Any:
        import cadquery as cq

        return cq.Workplane(obj=shape)


__all__ = ["RiexNc70GeometryProvider"]
