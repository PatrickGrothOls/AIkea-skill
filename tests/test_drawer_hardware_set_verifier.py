"""Scope: Verify the complete source-CAD gate for one selected drawer runner."""

from dataclasses import replace
from importlib.util import find_spec
import os
from pathlib import Path
import unittest

import pytest

from drawer_hardware_set_verifier import (
    DrawerHardwareSetVerifier,
    SOURCE_CAD_VERIFIED_UNPLACED,
)
from hardware_asset_manifest import HardwareAssetState
from hardware_asset_resolver import HardwareAssetError
from movento_runner_catalog import MOVENTO_760H5000S, MOVENTO_760H5500S


class TestDrawerHardwareSetContract:
    """Reject incomplete source proof before any STEP import can begin."""

    def test_does_not_fall_back_when_selected_depth_needs_the_550_runner(
        self,
        tmp_path: Path,
    ) -> None:
        verifier = DrawerHardwareSetVerifier(tmp_path)

        with pytest.raises(ValueError, match="760H5500S.*no complete"):
            verifier.verify(MOVENTO_760H5500S)

    def test_rejects_handed_identity_drift_before_reading_local_files(
        self,
        tmp_path: Path,
    ) -> None:
        verifier = DrawerHardwareSetVerifier(tmp_path)
        hardware = MOVENTO_760H5000S.require_hardware_asset_set()
        wrong_hand = replace(hardware.runner_left, handedness="right")
        profile = replace(
            MOVENTO_760H5000S,
            hardware_asset_set=replace(hardware, runner_left=wrong_hand),
        )

        with pytest.raises(HardwareAssetError, match="identity is incomplete"):
            verifier.verify(profile)

    @pytest.mark.parametrize(
        "record_change",
        (
            {"state": HardwareAssetState.INSPECTION_ONLY},
            {"expected_sha256": None},
            {"native_step_observation": None},
            {"embedded_product_codes": ()},
            {"handedness_basis": None},
        ),
    )
    def test_rejects_incomplete_registered_source_proof(
        self,
        tmp_path: Path,
        record_change: dict[str, object],
    ) -> None:
        verifier = DrawerHardwareSetVerifier(tmp_path)
        asset_id = "movento-760h5000s-runner-left"
        changed = replace(verifier.manifest.asset(asset_id), **record_change)
        verifier.manifest = replace(
            verifier.manifest,
            assets=tuple(
                changed if asset.asset_id == asset_id else asset
                for asset in verifier.manifest.assets
            ),
        )

        with pytest.raises(HardwareAssetError, match="identity is incomplete"):
            verifier.verify(MOVENTO_760H5000S)


@unittest.skipUnless(
    find_spec("cadquery") and os.environ.get("AIKEA_BLUM_DOWNLOAD_DIR"),
    "requires CadQuery and AIKEA_BLUM_DOWNLOAD_DIR",
)
class TestDownloadedDrawerHardwareSet(unittest.TestCase):
    """Admit the four exact manufacturer files as one unplaced hardware set."""

    def test_verifies_the_complete_500_mm_hardware_set(self) -> None:
        verified = DrawerHardwareSetVerifier(
            Path(os.environ["AIKEA_BLUM_DOWNLOAD_DIR"])
        ).verify(MOVENTO_760H5000S)

        self.assertEqual(verified.geometry_state, SOURCE_CAD_VERIFIED_UNPLACED)
        self.assertEqual(
            (
                verified.runner_left.asset.record.asset_id,
                verified.runner_right.asset.record.asset_id,
                verified.locking_device_left.asset.record.asset_id,
                verified.locking_device_right.asset.record.asset_id,
            ),
            tuple(
                identity.asset_id
                for identity in MOVENTO_760H5000S.require_hardware_asset_set().identities()
            ),
        )


if __name__ == "__main__":
    unittest.main()
