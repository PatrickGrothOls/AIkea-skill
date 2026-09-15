"""Scope: Checksum-gate and classify the unchanged four-member Hettich 9114274 STEP."""
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetResolver
from hardware_step_importer import HardwareStepImporter, ImportedHardwareStep
from hettich_ka_4532_400_profile import HETTICH_KA_4532_400


@dataclass(frozen=True, slots=True)
class HettichKa4532FourHundredStepSet:
    source: ImportedHardwareStep
    members: dict[str, Any]


class HettichKa4532FourHundredClassifier:
    """Name roles by this source's bounds and volume, independently of STEP import order."""

    signatures = {
        "left-fixed": (0, 8.777139874, -9.5, 392.983917012, -22.85009328, 22.85009328, 37318.87023579),
        "left-moving": (4.2, 12.5, -9.5, 390.54, -12.149518924, 12.149518924, 19221.987116394),
        "right-moving": (188.5, 196.8, -9.5, 390.54, -12.149518924, 12.149518924, 19221.987116394),
        "right-fixed": (192.222860126, 201, -9.5, 392.983917012, -22.85009328, 22.85009328, 37318.870271459),
    }

    def classify(self, solids):
        members = {}
        for solid in solids:
            if not solid.isValid():
                raise ValueError("9114274 source contains an invalid solid")
            bounds = solid.BoundingBox()
            values = tuple(getattr(bounds, key) for key in ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"))+(solid.Volume(),)
            matches = [role for role, signature in self.signatures.items()
                       if all(abs(a-b) <= .001 for a, b in zip(values, signature, strict=True))]
            if len(matches) != 1:
                raise ValueError("solid does not match exact 400 mm article 9114274")
            if matches[0] in members:
                raise ValueError("9114274 member set is duplicated")
            members[matches[0]] = solid
        if set(members) != set(self.signatures):
            raise ValueError("9114274 member set is incomplete")
        return members


class HettichKa4532FourHundredStepLoader:
    manifest_path = Path(__file__).resolve().parents[1]/"assets/hettich/ka-4532-400/hardware-assets.json"

    def load(self, source_directory):
        record = HardwareAssetManifest.load(self.manifest_path).asset(HETTICH_KA_4532_400.asset_id)
        asset = HardwareAssetResolver(Path(source_directory)).resolve(record)
        asset.require_build_ready()
        source = HardwareStepImporter().import_unchanged(asset)
        members = HettichKa4532FourHundredClassifier().classify(tuple(source.shape.Solids()))
        return HettichKa4532FourHundredStepSet(source, members)
