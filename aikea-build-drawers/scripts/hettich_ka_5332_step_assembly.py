"""Scope: Split the verified KA 5332 pair STEP into its six moving members."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter, ImportedHardwareStep
from hettich_ka_5332_runner_profile import HETTICH_KA_5332_500


@dataclass(frozen=True, slots=True)
class HettichKa5332SideStepParts:
    """Name the fixed, intermediate, and drawer-owned members on one hand."""

    cabinet_member: Any
    middle_member: Any
    drawer_member: Any


@dataclass(frozen=True, slots=True)
class HettichKa5332StepAssembly:
    """Carry both handed mechanisms in unchanged manufacturer coordinates."""

    source: ImportedHardwareStep
    left: HettichKa5332SideStepParts
    right: HettichKa5332SideStepParts


class HettichKa5332StepAssemblyLoader:
    """Verify the paired STEP and classify members by native side and height."""

    _MANIFEST = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "hettich"
        / "ka-5332"
        / "hardware-assets.json"
    )

    def load(
        self,
        hardware_directory: Path,
    ) -> HettichKa5332StepAssembly:
        manifest = HardwareAssetManifest.load(self._MANIFEST)
        record = manifest.asset(HETTICH_KA_5332_500.asset_id)
        asset = HardwareAssetResolver(hardware_directory).resolve(record)
        asset.require_build_ready()
        imported = HardwareStepImporter().import_unchanged(asset)
        solids = tuple(imported.shape.Solids())
        split_x_mm = (
            imported.bounds_mm.xmin + imported.bounds_mm.xmax
        ) / 2.0
        left = tuple(solid for solid in solids if solid.Center().x < split_x_mm)
        right = tuple(solid for solid in solids if solid.Center().x > split_x_mm)
        return HettichKa5332StepAssembly(
            source=imported,
            left=self._classify_members(left),
            right=self._classify_members(right),
        )

    def _classify_members(
        self,
        solids: tuple[Any, ...],
    ) -> HettichKa5332SideStepParts:
        drawer, middle, cabinet = sorted(
            solids,
            key=lambda solid: solid.BoundingBox().zlen,
        )
        return HettichKa5332SideStepParts(
            cabinet_member=cabinet,
            middle_member=middle,
            drawer_member=drawer,
        )


__all__ = [
    "HettichKa5332SideStepParts",
    "HettichKa5332StepAssembly",
    "HettichKa5332StepAssemblyLoader",
]
