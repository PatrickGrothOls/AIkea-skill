"""Scope: Preserve source geometry and deliberate lighting while applying presentation defaults."""

from copy import deepcopy
import hashlib
import json
import struct
import sys
from unittest.mock import patch

from bake_furniture_presentation import FurniturePresentationCommand
from presentation_light_defaults import PresentationLightDefaults


class TestPresentationLightDefaults:
    def source(self, root):
        led = {"emissiveFactor": [1, 1, 1], "extras": {"aikea": {
            "appearance_status": "representative_output", "photometric_calibration": False}},
            "extensions": {"KHR_materials_emissive_strength": {"emissiveStrength": 5}}}
        calibrated = deepcopy(led)
        calibrated["extras"]["aikea"]["photometric_calibration"] = True
        override = deepcopy(led)
        override["extras"]["aikea"]["preserve_emission"] = True
        document = {"asset": {"version": "2.0"}, "scene": 0,
            "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}],
            "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "material": 0}]}],
            "buffers": [{"byteLength": 12}], "bufferViews": [{"buffer": 0, "byteLength": 12}],
            "accessors": [{"bufferView": 0, "componentType": 5126, "count": 1, "type": "VEC3"}],
            "materials": [led, calibrated, override, {"name": "wood", "emissiveFactor": [0, 0, 0]}]}
        path = root / "source.glb"
        self.write(path, document, struct.pack("<II3f", 12, 0x004E4942, 0, 0, 0))
        return path

    def write(self, path, document, tail):
        encoded = json.dumps(document).encode()
        encoded += b" " * (-len(encoded) % 4)
        chunks = struct.pack("<II", len(encoded), 0x4E4F534A) + encoded + tail
        path.write_bytes(struct.pack("<4sII", b"glTF", 2, len(chunks) + 12) + chunks)

    def read(self, path):
        raw = path.read_bytes()
        length = struct.unpack_from("<I", raw, 12)[0]
        return json.loads(raw[20:20 + length]), raw[20 + length:]

    def test_only_representative_emission_changes_and_original_is_untouched(self, tmp_path):
        source = self.source(tmp_path)
        original_bytes = source.read_bytes()
        before, binary = self.read(source)
        result = PresentationLightDefaults().prepare(source, tmp_path)
        after, result_binary = self.read(result)
        assert source.read_bytes() == original_bytes
        assert result_binary == binary
        expected = deepcopy(before)
        expected["materials"][0]["extensions"]["KHR_materials_emissive_strength"]["emissiveStrength"] = 40
        expected["extensionsUsed"] = ["KHR_materials_emissive_strength"]
        assert after == expected
        assert PresentationLightDefaults().prepare(result, tmp_path) == result

    def test_no_declared_emitters_leaves_source_path_unchanged(self, tmp_path):
        source = self.source(tmp_path)
        document, tail = self.read(source)
        document["materials"] = [{"emissiveFactor": [1, 1, 1]}]
        self.write(source, document, tail)
        assert PresentationLightDefaults().prepare(source, tmp_path) == source
        assert not (tmp_path / "inspection-materials.glb").exists()

    def test_cli_snapshots_prepared_source_for_both_bake_and_inspection(self, tmp_path):
        source = self.source(tmp_path)
        output = tmp_path / "bake"
        argv = ["bake", str(source), str(output), "--runtime-directory", str(tmp_path / "runtime")]
        with patch.object(sys, "argv", argv), \
                patch("bake_furniture_presentation.BlenderBakeRuntime.command", return_value=["fake"]), \
                patch("bake_furniture_presentation.subprocess.run"), \
                patch("builtins.print"), \
                patch("pathlib.Path.read_text", return_value="{}"):
            FurniturePresentationCommand().run()
        config = json.loads((output / "job.json").read_text())
        assert config["source"] == str(output / "inspection-materials.glb")
        assert config["source_sha256"] == hashlib.sha256((output / "inspection-materials.glb").read_bytes()).hexdigest()
        assert config["threads"] == 1
        assert config["samples"] == 16
        assert config["atlas_size"] == 4096
