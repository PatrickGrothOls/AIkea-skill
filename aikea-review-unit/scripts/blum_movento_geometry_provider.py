"""Scope: Load exact registered Blum MOVENTO hardware from project storage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from drawer_hardware_set_verifier import DEFAULT_MANIFEST_PATH
from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter


class BlumMoventoGeometryProvider:
    """Verify and cache individual MOVENTO source-CAD components."""

    def __init__(self) -> None:
        self.manifest = HardwareAssetManifest.load(DEFAULT_MANIFEST_PATH)
        self.assets = {asset.asset_id for asset in self.manifest.assets}
        self.importer = HardwareStepImporter()
        self.cache: dict[tuple[Path, str], Any] = {}

    def supports(self, asset_id: str) -> bool:
        return asset_id in self.assets

    def resolve(self, project_root: Path, spec: Any) -> Any:
        key = (project_root.resolve(), spec.hardware_asset_id)
        if key not in self.cache:
            record = self.manifest.asset(spec.hardware_asset_id)
            source = (
                project_root
                / "hardware/blum/movento"
                / str(record.catalog_item_number)
                / "source"
            )
            asset = HardwareAssetResolver(source).resolve(record)
            asset.require_build_ready()
            imported = self.importer.import_unchanged(asset)
            self.cache[key] = self._workplane(imported.shape)
        return self.cache[key]

    def _workplane(self, shape: Any) -> Any:
        import cadquery as cq

        return cq.Workplane(obj=shape)


__all__ = ["BlumMoventoGeometryProvider"]
