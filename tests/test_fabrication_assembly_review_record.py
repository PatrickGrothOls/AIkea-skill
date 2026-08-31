"""Scope: Verify visual approval is bound to exact closed assembly bytes."""

from __future__ import annotations

import json

from fabrication_assembly_review_record import FabricationAssemblyReviewRecord


class TestFabricationAssemblyReviewRecord:
    """Protect proposal renewal without discarding a current approval."""

    def test_preserves_approval_for_the_unchanged_model(self, tmp_path) -> None:
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        model.parent.mkdir(parents=True)
        model.write_bytes(b"first")
        writer = FabricationAssemblyReviewRecord()
        record = writer.write_proposal(tmp_path, model)
        approved = json.loads(record.read_text(encoding="utf-8"))
        approved["status"] = "approved"
        record.write_text(json.dumps(approved), encoding="utf-8")

        writer.write_proposal(tmp_path, model)

        assert json.loads(record.read_text(encoding="utf-8"))["status"] == "approved"

    def test_changed_model_requires_a_new_visual_decision(self, tmp_path) -> None:
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        model.parent.mkdir(parents=True)
        model.write_bytes(b"first")
        writer = FabricationAssemblyReviewRecord()
        record = writer.write_proposal(tmp_path, model)
        approved = json.loads(record.read_text(encoding="utf-8"))
        approved["status"] = "approved"
        record.write_text(json.dumps(approved), encoding="utf-8")
        model.write_bytes(b"second")

        writer.write_proposal(tmp_path, model)

        saved = json.loads(record.read_text(encoding="utf-8"))
        assert saved["status"] == "proposed"
        assert saved["artifact"] == "assemblies/full_wardrobe_review.glb"


__all__ = ["TestFabricationAssemblyReviewRecord"]
