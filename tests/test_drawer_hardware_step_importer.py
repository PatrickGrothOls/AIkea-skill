"""Scope: Verify downloaded Blum STEP files remain in manufacturer coordinates."""

from importlib.util import find_spec
import os
from pathlib import Path
import unittest

from hardware_asset_manifest import HardwareAssetManifest
from hardware_asset_resolver import HardwareAssetError, HardwareAssetResolver
from hardware_step_importer import (
    HardwareStepImporter,
    STEP_NATIVE_MILLIMETRE_FRAME,
)


@unittest.skipUnless(
    find_spec("cadquery") and os.environ.get("AIKEA_BLUM_DOWNLOAD_DIR"),
    "requires CadQuery and AIKEA_BLUM_DOWNLOAD_DIR",
)
class TestDownloadedDrawerHardwareStepAssets(unittest.TestCase):
    """Integrate the exact downloaded files without copying them into the skill."""

    _MANIFEST_PATH = (
        Path(__file__).parents[1]
        / "aikea-build-drawers"
        / "assets"
        / "blum"
        / "movento"
        / "hardware-assets.json"
    )

    def test_downloaded_assets_match_native_observations(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        download_root = Path(os.environ["AIKEA_BLUM_DOWNLOAD_DIR"])
        resolver = HardwareAssetResolver(download_root)
        importer = HardwareStepImporter()

        for record in manifest.assets:
            if not record.download_filename:
                continue
            with self.subTest(asset=record.asset_id):
                resolved = resolver.resolve(
                    record,
                    download_root / record.download_filename,
                )
                imported = importer.import_unchanged(resolved)

                self.assertEqual(
                    imported.manufacturer_frame,
                    STEP_NATIVE_MILLIMETRE_FRAME,
                )
                self.assertEqual(
                    imported.solid_count,
                    record.native_step_observation.solid_count,
                )
                self.assertEqual(
                    imported.bounds_mm.values(),
                    record.native_step_observation.bounds_mm.values(),
                )

    def test_one_handed_550_candidate_remains_inspection_only(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        record = manifest.asset("movento-760h5500s-runner-candidate")
        download_root = Path(os.environ["AIKEA_BLUM_DOWNLOAD_DIR"])
        resolved = HardwareAssetResolver(download_root).resolve(
            record,
            download_root / record.download_filename,
        )

        with self.assertRaisesRegex(HardwareAssetError, "inspection-only"):
            resolved.require_build_ready()


if __name__ == "__main__":
    unittest.main()
