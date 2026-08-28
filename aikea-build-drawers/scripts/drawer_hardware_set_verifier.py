"""Scope: Admit one exact source-CAD hardware set before drawer generation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hardware_asset_manifest import (
    HardwareAssetManifest,
    HardwareAssetRecord,
    HardwareAssetState,
)
from hardware_asset_resolver import HardwareAssetError, HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter, ImportedHardwareStep
from movento_runner_profile import MoventoHardwareAssetIdentity, MoventoRunnerProfile


SOURCE_CAD_VERIFIED_UNPLACED = "source_cad_verified_unplaced"
DEFAULT_MANIFEST_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "blum"
    / "movento"
    / "hardware-assets.json"
)


@dataclass(frozen=True, slots=True)
class VerifiedDrawerHardwareSet:
    """Carry imported source CAD without implying an installation transform."""

    runner_left: ImportedHardwareStep
    runner_right: ImportedHardwareStep
    locking_device_left: ImportedHardwareStep
    locking_device_right: ImportedHardwareStep
    geometry_state: str = SOURCE_CAD_VERIFIED_UNPLACED


class DrawerHardwareSetVerifier:
    """Verify the complete depth-matched runner and locking-device set."""

    def __init__(
        self,
        hardware_directory: Path,
        manifest_path: Path = DEFAULT_MANIFEST_PATH,
    ) -> None:
        self.manifest = HardwareAssetManifest.load(manifest_path)
        self.resolver = HardwareAssetResolver(hardware_directory)
        self.importer = HardwareStepImporter()

    def verify(self, runner: MoventoRunnerProfile) -> VerifiedDrawerHardwareSet:
        asset_set = runner.require_hardware_asset_set()
        identities = asset_set.identities()
        imported = tuple(self._verify_component(identity) for identity in identities)
        return VerifiedDrawerHardwareSet(
            runner_left=imported[0],
            runner_right=imported[1],
            locking_device_left=imported[2],
            locking_device_right=imported[3],
        )

    def _verify_component(
        self,
        identity: MoventoHardwareAssetIdentity,
    ) -> ImportedHardwareStep:
        record = self.manifest.asset(identity.asset_id)
        self._require_identity(record, identity)
        resolved = self.resolver.resolve(record)
        resolved.require_build_ready()
        return self.importer.import_unchanged(resolved)

    def _require_identity(
        self,
        record: HardwareAssetRecord,
        identity: MoventoHardwareAssetIdentity,
    ) -> None:
        identity_matches = (
            record.state is HardwareAssetState.READY,
            record.component_type == identity.component_type,
            record.product_code == identity.product_code,
            record.catalog_item_number == identity.item_number,
            record.handedness == identity.handedness,
            bool(record.handedness_basis),
            bool(record.embedded_product_codes),
            bool(record.expected_sha256),
            record.native_step_observation is not None,
        )
        if not all(identity_matches):
            raise HardwareAssetError(
                f"registered hardware identity is incomplete for {identity.asset_id}"
            )


@dataclass(frozen=True, slots=True)
class DrawerHardwareSetVerifierFactory:
    """Create project-run verifiers against one versioned asset manifest."""

    manifest_path: Path = DEFAULT_MANIFEST_PATH

    def create(self, hardware_directory: Path) -> DrawerHardwareSetVerifier:
        return DrawerHardwareSetVerifier(hardware_directory, self.manifest_path)


__all__ = [
    "DEFAULT_MANIFEST_PATH",
    "DrawerHardwareSetVerifier",
    "DrawerHardwareSetVerifierFactory",
    "SOURCE_CAD_VERIFIED_UNPLACED",
    "VerifiedDrawerHardwareSet",
]
