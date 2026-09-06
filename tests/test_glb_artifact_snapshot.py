"""Scope: Reject structurally empty GLB review artifacts."""

from __future__ import annotations

import json
import struct

import pytest

from glb_artifact_snapshot import GlbArtifactSnapshot
from unit_mockup import UnitMockupInputError


class TestGlbArtifactSnapshot:
    """Require review artifacts to expose mesh geometry in the default scene."""

    @pytest.mark.parametrize(
        "document",
        (
            {
                "asset": {"version": "2.0"},
                "scene": 0,
                "scenes": [{"nodes": []}],
                "nodes": [],
                "meshes": [],
            },
            {
                "asset": {"version": "2.0"},
                "scene": 0,
                "scenes": [{"nodes": [0]}],
                "nodes": [{}, {"mesh": 0}],
                "meshes": [{"primitives": [{}]}],
            },
            {
                "asset": {"version": "2.0"},
                "scene": 0,
                "scenes": [{"nodes": [0]}],
                "nodes": [{"mesh": 0}],
                "meshes": [{"primitives": [{}]}],
            },
        ),
    )
    def test_rejects_default_scene_without_reachable_mesh(
        self,
        tmp_path,
        document,
    ) -> None:
        path = tmp_path / "empty.glb"
        path.write_bytes(self._glb_bytes(document))

        with pytest.raises(UnitMockupInputError, match="renderable default scene"):
            GlbArtifactSnapshot.load(path)

    @staticmethod
    def _glb_bytes(document: dict) -> bytes:
        encoded = json.dumps(document, separators=(",", ":")).encode("utf-8")
        encoded += b" " * (-len(encoded) % 4)
        chunk = struct.pack("<II", len(encoded), 0x4E4F534A) + encoded
        return struct.pack("<4sII", b"glTF", 2, 12 + len(chunk)) + chunk


__all__ = ["TestGlbArtifactSnapshot"]
