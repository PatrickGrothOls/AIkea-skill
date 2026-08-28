"""Scope: Export verified drawer locking devices for native-CAD inspection only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cadquery as cq

from cadquery_glb_exporter import CadQueryGlbExporter
from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter
from unit_mockup import MockupPart


@dataclass(frozen=True, slots=True)
class LockingDeviceReviewResult:
    """Identify the native-CAD inspection artifact without implying installation."""

    glb_path: Path
    asset_ids: tuple[str, ...]
    placement_state: str


class LockingDeviceReviewGenerator:
    """Export the verified left and right T51 devices in their vendor frames."""

    _ASSET_IDS = (
        "t51-7601-left-locking-device",
        "t51-7601-right-locking-device",
    )
    _METAL_COLOR = (0.30, 0.34, 0.38, 1.0)

    def __init__(self, manifest_path: Path, hardware_directory: Path) -> None:
        self.manifest = HardwareAssetManifest.load(manifest_path)
        self.resolver = HardwareAssetResolver(hardware_directory)
        self.importer = HardwareStepImporter()
        self.exporter = CadQueryGlbExporter()

    def generate(self, output_path: Path) -> LockingDeviceReviewResult:
        """Write untouched handed device geometry in a shared inspection scene."""
        parts = tuple(
            self._native_part(asset_id)
            for asset_id in self._ASSET_IDS
        )
        self.exporter.export(
            "t51_7601_locking_devices_native_cad_inspection",
            parts,
            output_path,
        )
        return LockingDeviceReviewResult(
            glb_path=output_path,
            asset_ids=self._ASSET_IDS,
            placement_state="vendor_native_frames_unmounted",
        )

    def _native_part(self, asset_id: str) -> MockupPart:
        record = self.manifest.asset(asset_id)
        if record.download_filename is None:
            raise ValueError(f"{asset_id} does not identify its downloaded STEP file")
        asset = self.resolver.resolve(
            record,
            self.resolver.asset_root / record.download_filename,
        )
        asset.require_build_ready()
        imported = self.importer.import_unchanged(asset)
        return MockupPart(
            f"review_only__{asset_id}__native_cad",
            cq.Workplane(obj=imported.shape),
            cq.Location(),
            self._METAL_COLOR,
        )


__all__ = [
    "LockingDeviceReviewGenerator",
    "LockingDeviceReviewResult",
]
