"""Scope: Verify recursive review reports earn valid status from real artifacts."""

from __future__ import annotations

from hashlib import sha256
import json

import cadquery as cq
import pytest

from cadquery_glb_exporter import CadQueryGlbExporter
from complete_assembly_review_report import CompleteAssemblyReviewReport
from unit_mockup import MockupPart, UnitMockupInputError


class TestCompleteAssemblyReviewReport:
    """Protect checksum, contents, and refusal paths in the real report writer."""

    def test_writes_validated_checksum_bounds_and_feature_states(self, tmp_path) -> None:
        part = self._box("cabinet_01__side", (5.0, 6.0, 7.0))
        glb_path = tmp_path / "cabinet.glb"
        CadQueryGlbExporter().export("cabinet_01", (part,), glb_path)

        report_path = CompleteAssemblyReviewReport().write(
            "cabinet_01",
            glb_path,
            (part,),
            {"cabinet_01/door": "open"},
        )

        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["status"] == "valid"
        assert report["manufacturing_authority"] is False
        assert report["artifact_sha256"] == sha256(glb_path.read_bytes()).hexdigest()
        assert report["part_count"] == 1
        assert report["feature_states"] == {"cabinet_01/door": "open"}
        assert report["items"] == [
            {
                "name": "cabinet_01__side",
                "bounds_mm": {
                    "x": [5.0, 15.0],
                    "y": [6.0, 26.0],
                    "z": [7.0, 37.0],
                },
            }
        ]

    @pytest.mark.parametrize("content", (b"", b"not a glb"))
    def test_rejects_a_missing_or_corrupt_glb(self, tmp_path, content) -> None:
        glb_path = tmp_path / "cabinet.glb"
        if content:
            glb_path.write_bytes(content)

        with pytest.raises(UnitMockupInputError, match="GLB"):
            CompleteAssemblyReviewReport().write(
                "cabinet_01",
                glb_path,
                (self._box("side", (0.0, 0.0, 0.0)),),
                {},
            )

        assert not glb_path.with_suffix(".review.json").exists()

    def test_rejects_an_empty_part_collection(self, tmp_path) -> None:
        glb_path = self._glb(tmp_path)

        with pytest.raises(UnitMockupInputError, match="no parts"):
            CompleteAssemblyReviewReport().write(
                "cabinet_01",
                glb_path,
                (),
                {},
            )

    def test_rejects_duplicate_part_names(self, tmp_path) -> None:
        glb_path = self._glb(tmp_path)
        parts = self._box("side", (0.0, 0.0, 0.0)), self._box(
            "side",
            (20.0, 0.0, 0.0),
        )

        with pytest.raises(UnitMockupInputError, match="unique"):
            CompleteAssemblyReviewReport().write(
                "cabinet_01",
                glb_path,
                parts,
                {},
            )

    def test_rejects_zero_volume_geometry(self, tmp_path) -> None:
        glb_path = self._glb(tmp_path)
        wire = MockupPart(
            "outline",
            cq.Workplane("XY").rect(10.0, 20.0).wire(),
            cq.Location(),
            (1.0, 1.0, 1.0, 1.0),
        )

        with pytest.raises(UnitMockupInputError, match="invalid geometry"):
            CompleteAssemblyReviewReport().write(
                "cabinet_01",
                glb_path,
                (wire,),
                {},
            )

    def _glb(self, root):
        path = root / "cabinet.glb"
        CadQueryGlbExporter().export(
            "cabinet_01",
            (self._box("side", (0.0, 0.0, 0.0)),),
            path,
        )
        return path

    def _box(self, name, origin):
        return MockupPart(
            name,
            cq.Workplane("XY").box(
                10.0,
                20.0,
                30.0,
                centered=(False, False, False),
            ),
            cq.Location(cq.Vector(*origin)),
            (1.0, 1.0, 1.0, 1.0),
        )


__all__ = ["TestCompleteAssemblyReviewReport"]
