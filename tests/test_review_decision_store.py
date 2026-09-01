"""Scope: Verify local decisions are atomic and bound to served artifacts."""

from __future__ import annotations

from hashlib import sha256
import json

import cadquery as cq
import pytest

from cadquery_glb_exporter import CadQueryGlbExporter
from glb_artifact_snapshot import GlbArtifactSnapshot
from review_decision_store import ReviewDecisionConflict, ReviewDecisionStore
from unit_mockup import MockupPart


class TestReviewDecisionStore:
    """Protect the single proposal transition and exact fabrication binding."""

    def test_approval_confirms_the_proposed_local_opening(self, tmp_path) -> None:
        path = self._door_record(tmp_path)

        result = ReviewDecisionStore(path).decide("approved")

        assert result["status"] == "approved"
        assert "decided_at" in result
        assert json.loads(path.read_text(encoding="utf-8"))["doors"][0][
            "hinge_side"
        ] == "left"

    def test_unknown_decision_does_not_change_the_record(self, tmp_path) -> None:
        path = self._door_record(tmp_path)
        before = path.read_text(encoding="utf-8")

        with pytest.raises(ValueError, match="unsupported"):
            ReviewDecisionStore(path).decide("maybe")

        assert path.read_text(encoding="utf-8") == before

    def test_fabrication_approval_records_the_served_checksum(self, tmp_path) -> None:
        model = self._model(tmp_path, "review.glb", 10.0)
        path = self._fabrication_record(tmp_path, model)
        artifact = GlbArtifactSnapshot.load(model)

        result = ReviewDecisionStore(path).decide("approved", artifact)

        assert result["status"] == "approved"
        assert result["artifact_sha256"] == artifact.sha256
        assert result["decision_artifact_sha256"] == artifact.sha256

    def test_rejects_a_different_served_model_without_writing(self, tmp_path) -> None:
        proposed = self._model(tmp_path, "proposed.glb", 10.0)
        served = self._model(tmp_path, "served.glb", 20.0)
        path = self._fabrication_record(tmp_path, proposed)
        before = path.read_text(encoding="utf-8")

        with pytest.raises(ReviewDecisionConflict, match="served GLB"):
            ReviewDecisionStore(path).decide(
                "approved",
                GlbArtifactSnapshot.load(served),
            )

        assert path.read_text(encoding="utf-8") == before

    def test_a_second_decision_cannot_overwrite_the_first(self, tmp_path) -> None:
        path = self._door_record(tmp_path)
        store = ReviewDecisionStore(path)
        store.decide("approved")

        with pytest.raises(ReviewDecisionConflict, match="no longer pending"):
            store.decide("change_requested")

        assert json.loads(path.read_text(encoding="utf-8"))["status"] == "approved"

    def _door_record(self, root):
        path = root / "reviews/door-openings.json"
        self._write_json(
            path,
            {
                "review_type": "door_openings",
                "status": "proposed",
                "message": "Review the door.",
                "doors": [
                    {
                        "assembly_id": "cabinet_01",
                        "hinge_side": "left",
                    }
                ],
            },
        )
        return path

    def _fabrication_record(self, root, model):
        path = root / "reviews/fabrication-assembly.json"
        self._write_json(
            path,
            {
                "review_type": "fabrication_assembly",
                "status": "proposed",
                "message": "Approve this exact assembly.",
                "artifact": str(model.relative_to(root)),
                "artifact_sha256": sha256(model.read_bytes()).hexdigest(),
            },
        )
        return path

    def _model(self, root, name, size):
        path = root / "assemblies" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        CadQueryGlbExporter().export(
            "wardrobe_01",
            (
                MockupPart(
                    "panel",
                    cq.Workplane("XY").box(size, 10.0, 10.0),
                    cq.Location(),
                    (0.8, 0.7, 0.6, 1.0),
                ),
            ),
            path,
        )
        return path

    def _write_json(self, path, value) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")


__all__ = ["TestReviewDecisionStore"]
