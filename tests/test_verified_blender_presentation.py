"""Scope: Reject missing, failed, stale and insufficient Blender presentation evidence."""

import json
from unittest.mock import patch

import pytest

from blender_presentation_test_evidence import BlenderPresentationTestEvidence
from review_server_test_support import ReviewServerTestSupport
from review_server_session import ReviewServerSession
from serve_unit_review import ServeUnitReviewCommand


class TestVerifiedBlenderPresentation:
    @pytest.mark.parametrize("filename,key,value", [
        ("presentation.json", "status", "FAIL"),
        ("presentation.json", "source_sha256", "stale"),
        ("presentation.json", "assembled_sha256", "stale"),
        ("presentation.json", "checks", []),
        ("presentation.json", "atlas_size", 512),
        ("presentation.json", "samples", 1),
        ("presentation.json", "maximum_vertex_error_mm", float("nan")),
        ("prepared-geometry.json", "no_mesh_changes", False),
        ("shaded-geometry.json", "source_sha256", "stale"),
        ("all-panel-coverage.json", "uncovered_centroids", 1),
        ("export-geometry.json", "exported_sha256", "stale"),
        ("export-geometry.json", "tolerance_mm", 0.1),
        ("export-geometry.json", "status", "FAIL"),
    ])
    def test_incomplete_or_changed_evidence_blocks_session(self, tmp_path, filename, key, value):
        model, inspection = self._pair(tmp_path)
        path = model.parent / filename
        report = json.loads(path.read_text())
        report[key] = value
        path.write_text(json.dumps(report))
        with pytest.raises(ValueError, match="Blender"):
            ReviewServerSession(model, None, inspection)

    @pytest.mark.parametrize("changed", ["model", "inspection"])
    def test_changed_glb_bytes_invalidate_the_old_bake(self, tmp_path, changed):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model()
        inspection = support.write_model("inspection.glb")
        BlenderPresentationTestEvidence().write(model, inspection)
        support.write_model("model.glb" if changed == "model" else "inspection.glb", 20)
        with pytest.raises(ValueError, match="stale"):
            ReviewServerSession(model, None, inspection)

    @pytest.mark.parametrize("content", ["not json", "[]"])
    def test_malformed_report_is_a_clear_error(self, tmp_path, content):
        model, inspection = self._pair(tmp_path)
        (model.parent / "presentation.json").write_text(content)
        with pytest.raises(ValueError, match="Blender"):
            ReviewServerSession(model, None, inspection)

    def test_cli_rejects_raw_glb_before_starting_server(self, tmp_path, capsys):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model()
        with patch("unit_review_server.ThreadingHTTPServer") as socket:
            assert ServeUnitReviewCommand().run(model, 0, False, None) == 2
            socket.assert_not_called()
        assert "bake_furniture_presentation.py" in capsys.readouterr().out

    def test_missing_detail_report_blocks_even_when_summary_passes(self, tmp_path):
        model, inspection = self._pair(tmp_path)
        (model.parent / "export-geometry.json").unlink()
        with pytest.raises(ValueError, match="export-geometry.json"):
            ReviewServerSession(model, None, inspection)

    def _pair(self, root):
        support = ReviewServerTestSupport(root)
        model = support.write_model()
        inspection = support.write_model("inspection.glb")
        BlenderPresentationTestEvidence().write(model, inspection)
        return model, inspection
