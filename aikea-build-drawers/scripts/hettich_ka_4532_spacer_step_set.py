"""Scope: Load and classify the exact KA 4532 runner and 13952 spacer STEP set."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter, ImportedHardwareStep
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952
from hettich_ka_4532_step_signatures import HettichKa4532StepSignatureClassifier


@dataclass(frozen=True, slots=True)
class HettichKa4532RunnerSideStepParts:
    """Name the cabinet-fixed and drawer-moving members on one runner side."""

    fixed_member: Any
    moving_member: Any


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerStepSet:
    """Carry both runner hands and the unchanged purchased spacer geometry."""

    runner_source: ImportedHardwareStep
    spacer_source: ImportedHardwareStep
    runner_left: HettichKa4532RunnerSideStepParts
    runner_right: HettichKa4532RunnerSideStepParts
    spacer_solid: Any


class HettichKa4532SpacerStepSetLoader:
    """Resolve exact project-local assets and classify their native solids."""

    _MANIFEST = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "hettich"
        / "ka-4532-spacer"
        / "hardware-assets.json"
    )
    _RUNNER_SOURCE = Path(
        "hettich/ka-4532-silent-system/9114276/source"
    )
    _SPACER_SOURCE = Path(
        "hettich/ka-4532-spacer-profile/13952/source"
    )

    def load(self, hardware_root: Path) -> HettichKa4532SpacerStepSet:
        manifest = HardwareAssetManifest.load(self._MANIFEST)
        importer = HardwareStepImporter()
        profile = HETTICH_KA_4532_500_WITH_13952
        runner = self._load_unchanged(
            manifest,
            profile.runner_asset_id,
            hardware_root / self._RUNNER_SOURCE,
            importer,
        )
        spacer = self._load_unchanged(
            manifest,
            profile.spacer_asset_id,
            hardware_root / self._SPACER_SOURCE,
            importer,
        )
        classified = HettichKa4532StepSignatureClassifier().classify(
            tuple(runner.shape.Solids()),
            spacer.shape.Solids()[0],
        )
        return HettichKa4532SpacerStepSet(
            runner_source=runner,
            spacer_source=spacer,
            runner_left=HettichKa4532RunnerSideStepParts(
                fixed_member=classified.left_fixed,
                moving_member=classified.left_moving,
            ),
            runner_right=HettichKa4532RunnerSideStepParts(
                fixed_member=classified.right_fixed,
                moving_member=classified.right_moving,
            ),
            spacer_solid=classified.spacer,
        )

    def _load_unchanged(
        self,
        manifest: HardwareAssetManifest,
        asset_id: str,
        source_directory: Path,
        importer: HardwareStepImporter,
    ) -> ImportedHardwareStep:
        record = manifest.asset(asset_id)
        asset = HardwareAssetResolver(source_directory).resolve(record)
        asset.require_build_ready()
        return importer.import_unchanged(asset)

__all__ = [
    "HettichKa4532RunnerSideStepParts",
    "HettichKa4532SpacerStepSet",
    "HettichKa4532SpacerStepSetLoader",
]
