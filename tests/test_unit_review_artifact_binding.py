"""Scope: Verify viewer approval belongs to the exact GLB bytes it served."""

from __future__ import annotations

from hashlib import sha256
import json

import pytest

from review_decision_store import ReviewDecisionConflict
from review_server_test_support import ReviewServerTestSupport


class TestUnitReviewArtifactBinding:
    """Protect startup binding, immutable serving, and stale-record refusal."""

    def test_rejects_a_record_for_a_different_model_before_serving(
        self,
        tmp_path,
    ) -> None:
        support = ReviewServerTestSupport(tmp_path)
        proposed = support.write_model("proposed.glb", 10.0)
        served = support.write_model("served.glb", 20.0)
        review = self._record(support, proposed)

        with pytest.raises(ReviewDecisionConflict, match="served GLB"):
            support.start(served, review)

    def test_model_routes_serve_the_startup_snapshot_after_source_changes(
        self,
        tmp_path,
    ) -> None:
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model(size=10.0)
        startup_bytes = model.read_bytes()
        review = self._record(support, model)
        server = support.start(model, review)
        try:
            token = self._token(support, server)
            support.write_model(size=20.0)

            served_models = tuple(
                support.request(server, path)
                for path in ("model.glb", "model%2Eglb", "model%252Eglb")
            )
            decision_status, _content = support.request(
                server,
                "api/review-decision",
                "POST",
                {"decision": "approved"},
                self._headers(server, token),
            )
        finally:
            server.close()

        saved = json.loads(review.read_text(encoding="utf-8"))
        assert tuple(status for status, _content in served_models) == (200, 200, 200)
        assert all(content == startup_bytes for _status, content in served_models)
        assert model.read_bytes() != startup_bytes
        assert decision_status == 200
        assert saved["decision_artifact_sha256"] == sha256(startup_bytes).hexdigest()

    def test_rejects_a_record_changed_after_the_viewer_loaded(self, tmp_path) -> None:
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model()
        review = self._record(support, model)
        server = support.start(model, review)
        try:
            token = self._token(support, server)
            record = json.loads(review.read_text(encoding="utf-8"))
            record["artifact_sha256"] = "stale"
            review.write_text(json.dumps(record), encoding="utf-8")

            status, _content = support.request(
                server,
                "api/review-decision",
                "POST",
                {"decision": "approved"},
                self._headers(server, token),
            )
        finally:
            server.close()

        assert status == 409
        assert json.loads(review.read_text(encoding="utf-8"))["status"] == "proposed"

    def _record(self, support, model):
        return support.write_json(
            "reviews/fabrication-assembly.json",
            {
                "review_type": "fabrication_assembly",
                "status": "proposed",
                "message": "Approve this exact assembly.",
                "artifact": str(model.relative_to(support.root)),
                "artifact_sha256": sha256(model.read_bytes()).hexdigest(),
            },
        )

    def _token(self, support, server):
        status, content = support.request(server, "review-data.json")
        assert status == 200
        return json.loads(content)["decision_token"]

    def _headers(self, server, token):
        return {
            "Content-Type": "application/json",
            "Origin": server.url[:-1],
            "X-AIkea-Review-Token": token,
        }


__all__ = ["TestUnitReviewArtifactBinding"]
