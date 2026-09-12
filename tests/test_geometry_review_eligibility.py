"""Scope: Keep invalid or stale geometry out of proposal and live decision boundaries."""
import json

import pytest

from fabrication_assembly_review_record import FabricationAssemblyReviewRecord
from fabrication_review_proposal_writer import FabricationReviewProposalWriter
from full_wardrobe_review import FullWardrobeReviewResult
from review_server_test_support import ReviewServerTestSupport


class TestGeometryReviewEligibility:
    REPORT = "assemblies/construction-position-check.json"
    DIGEST = "current-construction"

    def result(self, root, status="valid"):
        return FullWardrobeReviewResult(("cabinet_01",), root / "assemblies/full_wardrobe_review.glb",
                                       root / "assemblies/full-wardrobe-position-check.json",
                                       {"cabinet_01": "closed"}, self.DIGEST, status, root / self.REPORT)

    def evidence(self, support, **overrides):
        return support.write_json(self.REPORT, dict(schema_version=2, status="valid",
                                                    construction_sha256=self.DIGEST) | overrides)

    @pytest.mark.parametrize("failure", ("missing", "malformed", "list", "invalid", "schema", "stale", "empty"))
    def test_ineligible_saved_evidence_never_creates_proposal(self, tmp_path, failure):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model("full_wardrobe_review.glb")
        before = model.read_bytes()
        path = self.evidence(support)
        contents = {"malformed": "{", "list": "[]", "invalid": json.dumps({"schema_version": 2, "status": "invalid"}),
                    "schema": json.dumps({"schema_version": 1, "status": "valid", "construction_sha256": self.DIGEST}),
                    "stale": json.dumps({"schema_version": 2, "status": "valid", "construction_sha256": "old"}),
                    "empty": json.dumps({"schema_version": 2, "status": "valid", "construction_sha256": ""})}
        if failure == "missing":
            path.unlink()
        else:
            path.write_text(contents[failure])
        assert FabricationReviewProposalWriter().write_for_result(tmp_path, self.result(tmp_path)) is None
        assert not (tmp_path / "reviews/fabrication-assembly.json").exists()
        assert model.read_bytes() == before

    @pytest.mark.parametrize("status", (None, "invalid"))
    def test_skipped_or_invalid_current_run_cannot_reuse_valid_saved_report(self, tmp_path, status):
        support = ReviewServerTestSupport(tmp_path)
        support.write_model("full_wardrobe_review.glb")
        self.evidence(support)
        assert FabricationReviewProposalWriter().write_for_result(tmp_path, self.result(tmp_path, status)) is None

    @pytest.mark.parametrize("approved", (False, True))
    def test_already_open_server_blocks_invalid_geometry_and_preserves_history(self, tmp_path, approved):
        support = ReviewServerTestSupport(tmp_path)
        model = support.write_model("full_wardrobe_review.glb")
        self.evidence(support)
        record = FabricationAssemblyReviewRecord().write_proposal(tmp_path, model, self.DIGEST)
        server = support.start(model, record)
        try:
            status, response = support.request(server, "review-data.json")
            assert status == 200
            token = json.loads(response)["decision_token"]
            headers = {"Content-Type": "application/json", "Origin": server.url[:-1],
                       "X-AIkea-Review-Token": token}
            if approved:
                status, _ = support.request(server, "api/review-decision", "POST", {"decision": "approved"}, headers)
                assert status == 200
            before, model_before = record.read_bytes(), model.read_bytes()
            self.evidence(support, status="invalid")
            assert FabricationReviewProposalWriter().write_for_result(tmp_path, self.result(tmp_path, "invalid")) is None
            assert support.request(server, "review-data.json")[0] == 409
            assert support.request(server, "api/review-decision", "POST", {"decision": "approved"}, headers)[0] == 409
            assert support.request(server, "model.glb") == (200, model_before)
            assert record.read_bytes() == before
        finally:
            server.close()
