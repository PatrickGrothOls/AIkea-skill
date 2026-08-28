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

        assert manifest.schema_version == 1
        assert manifest.vendor == "Blum"
        assert {asset.asset_id for asset in manifest.assets} == {
            "movento-760h5000s-runner-set",
            "movento-760h5500s-runner-candidate",
            "t51-7601-left-locking-device",
            "t51-7601-right-locking-device",
        }

    def test_unresolved_runner_cad_cannot_be_treated_as_build_ready(self) -> None:
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        runner_500 = manifest.asset("movento-760h5000s-runner-set")
        runner_550 = manifest.asset("movento-760h5500s-runner-candidate")

        assert runner_500.state is HardwareAssetState.REQUIRES_USER_DOWNLOAD
        assert runner_500.expected_sha256 is None
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

    def _test_record(self, contents: bytes):
        manifest = HardwareAssetManifest.load(self._MANIFEST_PATH)
        lock = manifest.asset("t51-7601-left-locking-device")
        return replace(
            lock,
            local_filename="test-hardware.step",
            expected_sha256=sha256(contents).hexdigest(),
        )
