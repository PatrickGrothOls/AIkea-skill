"""Scope: Verify the drawer skill records local hardware without STEP bytes."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path

import pytest

from hardware_asset_manifest import HardwareAssetManifest, HardwareAssetState
from hardware_asset_resolver import HardwareAssetError, HardwareAssetResolver


class TestDrawerHardwareAssetManifest:
    """Protect product identity, provenance, and unresolved CAD boundaries."""

    _SKILL_ROOT = Path(__file__).parents[1] / "aikea-build-drawers"
    _MANIFEST_PATH = (
        _SKILL_ROOT / "assets" / "blum" / "movento" / "hardware-assets.json"
    )

    def test_manifest_registers_both_runner_lengths_and_locking_devices(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)

        assert manifest.schema_version == 2
        assert manifest.vendor == "Blum"
        assert {asset.asset_id for asset in manifest.assets} == {
            "movento-760h5000s-runner-left",
            "movento-760h5000s-runner-right",
            "movento-760h5500s-runner-candidate",
            "t51-7601-left-locking-device",
            "t51-7601-right-locking-device",
        }

    def test_500_runner_pair_records_verified_handed_assets(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        left = manifest.asset("movento-760h5000s-runner-left")
        right = manifest.asset("movento-760h5000s-runner-right")

        assert left.state is HardwareAssetState.READY
        assert right.state is HardwareAssetState.READY
        assert left.handedness == "left"
        assert right.handedness == "right"
        assert "embedded-left-product-code" in left.handedness_basis
        assert "inference" in right.handedness_basis

    def test_incomplete_550_runner_cad_remains_inspection_only(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        runner_550 = manifest.asset("movento-760h5500s-runner-candidate")

        assert runner_550.state is HardwareAssetState.INSPECTION_ONLY
        assert "760H5501S" in runner_550.embedded_product_codes
        assert "one-handed" in runner_550.unresolved_reason

    def test_skill_contains_no_blum_step_bytes(self) -> None:
        assert not tuple(self._SKILL_ROOT.rglob("*.step"))
        assert not tuple(self._SKILL_ROOT.rglob("*.stp"))


class TestHardwareAssetResolver:
    """Verify known bytes before allowing a local asset into CAD import."""

    _MANIFEST_PATH = (
        Path(__file__).parents[1]
        / "aikea-build-drawers"
        / "assets"
        / "blum"
        / "movento"
        / "hardware-assets.json"
    )

    def test_resolves_a_matching_local_step(self, tmp_path: Path) -> None:
        record = self._test_record(b"verified step")
        path = tmp_path / record.local_filename
        path.write_bytes(b"verified step")

        resolved = HardwareAssetResolver(tmp_path).resolve(record)

        assert resolved.path == path.resolve()
        assert resolved.sha256 == record.expected_sha256
        resolved.require_build_ready()

    def test_rejects_changed_local_bytes(self, tmp_path: Path) -> None:
        record = self._test_record(b"expected")
        path = tmp_path / record.local_filename
        path.write_bytes(b"different")

        with pytest.raises(HardwareAssetError, match="checksum"):
            HardwareAssetResolver(tmp_path).resolve(record)

    def test_accepts_the_official_download_filename_without_renaming(
        self,
        tmp_path: Path,
    ) -> None:
        record = replace(
            self._test_record(b"official download"),
            download_filename="official-download.step",
        )
        downloaded = tmp_path / record.download_filename
        downloaded.write_bytes(b"official download")

        resolved = HardwareAssetResolver(tmp_path).resolve(record)

        assert resolved.path == downloaded.resolve()

    def test_skips_a_stale_alias_when_the_official_download_matches(
        self,
        tmp_path: Path,
    ) -> None:
        record = replace(
            self._test_record(b"official download"),
            download_filename="official-download.step",
        )
        (tmp_path / record.local_filename).write_bytes(b"stale alias")
        downloaded = tmp_path / record.download_filename
        downloaded.write_bytes(b"official download")

        resolved = HardwareAssetResolver(tmp_path).resolve(record)

        assert resolved.path == downloaded.resolve()

    def test_prefers_the_normalised_alias_when_both_files_match(
        self,
        tmp_path: Path,
    ) -> None:
        record = replace(
            self._test_record(b"matching bytes"),
            download_filename="official-download.step",
        )
        alias = tmp_path / record.local_filename
        alias.write_bytes(b"matching bytes")
        (tmp_path / record.download_filename).write_bytes(b"matching bytes")

        resolved = HardwareAssetResolver(tmp_path).resolve(record)

        assert resolved.path == alias.resolve()

    def _test_record(self, contents: bytes):
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        lock = manifest.asset("t51-7601-left-locking-device")
        return replace(
            lock,
            local_filename="test-hardware.step",
            expected_sha256=sha256(contents).hexdigest(),
        )
