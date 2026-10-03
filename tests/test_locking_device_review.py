"""Scope: Verify native T51 CAD exports without adding an installation transform."""

from importlib.util import find_spec
import json
from pathlib import Path
import os
import struct

import pytest


class GlbNodeNames:
    """Read only the node names needed to verify one exported review artifact."""

    def __init__(self, path: Path) -> None:
        contents = path.read_bytes()
        json_length, _ = struct.unpack("<I4s", contents[12:20])
        document = json.loads(contents[20 : 20 + json_length])
        self.names = {node["name"] for node in document["nodes"]}


@pytest.mark.skipif(
    not find_spec("cadquery") or not os.environ.get("AIKEA_BLUM_DOWNLOAD_DIR"),
    reason="requires CadQuery and AIKEA_BLUM_DOWNLOAD_DIR",
)
class TestLockingDeviceReviewGenerator:
    """Protect imported handed devices as native-CAD inspection geometry."""

    def test_exports_both_verified_devices_without_drawer_placement(
        self,
        tmp_path: Path,
    ) -> None:
        from locking_device_review import LockingDeviceReviewGenerator

        skill_root = Path(__file__).parents[1]
        manifest_path = (
            skill_root
            / "aikea-build-drawers"
            / "assets"
            / "blum"
            / "movento"
            / "hardware-assets.json"
        )
        result = LockingDeviceReviewGenerator(
            manifest_path,
            Path(os.environ["AIKEA_BLUM_DOWNLOAD_DIR"]),
        ).generate(tmp_path / "t51-devices.glb")

        document = GlbNodeNames(result.glb_path)

        assert {
            "review_only__t51-7601-left-locking-device__native_cad",
            "review_only__t51-7601-right-locking-device__native_cad",
        }.issubset(document.names)
        assert result.placement_state == "vendor_native_frames_unmounted"
