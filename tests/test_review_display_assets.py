"""Scope: Verify optional inspection files remain immutable and bounded to one local session."""

from hashlib import sha256
import json

from review_server_test_support import ReviewServerTestSupport
from unit_review_server import UnitReviewServer


class TestReviewDisplayAssets:
    """Separate display selection from approval authority and arbitrary filesystem access."""

    def test_optional_snapshot_and_manifest_keep_original_bytes(self, tmp_path):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model()
        inspection = support.write_model("inspection.glb", 12)
        primary_bytes, inspection_bytes = model.read_bytes(), inspection.read_bytes()
        server = UnitReviewServer(support.viewer, model, inspection_model_path=inspection)
        model.write_bytes(b"replaced after startup")
        inspection.unlink()
        try:
            status, body = support.request(server, "review-models.json")
            manifest = json.loads(body)
            assert status == 200
            assert manifest["assembled"]["sha256"] == sha256(primary_bytes).hexdigest()
            assert manifest["inspection"]["sha256"] == sha256(inspection_bytes).hexdigest()
            assert manifest["assembled"]["baked"] is True
            assert support.request(server, "model.glb") == (200, primary_bytes)
            assert support.request(server, "inspection.glb") == (200, inspection_bytes)
            for path in ("../assemblies/inspection.glb", "%252e%252e/assemblies/model.glb"):
                assert support.request(server, path)[0] == 404
        finally:
            server.close()

    def test_ordinary_single_model_remains_available_without_inspection(self, tmp_path):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model()
        server = UnitReviewServer(support.viewer, model)
        try:
            status, body = support.request(server, "review-models.json")
            manifest = json.loads(body)
            assert status == 200
            assert manifest["inspection"] is None
            assert manifest["assembled"]["baked"] is False
            assert support.request(server, "inspection.glb")[0] == 404
        finally:
            server.close()
