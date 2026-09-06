"""Scope: Verify visual approval is bound to exact closed assembly bytes."""

from __future__ import annotations

import json

import cadquery as cq

from cadquery_glb_exporter import CadQueryGlbExporter
from fabrication_assembly_review_record import FabricationAssemblyReviewRecord
from unit_mockup import MockupPart


class TestFabricationAssemblyReviewRecord:
    """Protect proposal renewal without discarding a current approval."""

    def test_preserves_approval_for_the_unchanged_model(self, tmp_path) -> None:
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        model.parent.mkdir(parents=True)
        self._write_model(model, 10.0)
        writer = FabricationAssemblyReviewRecord()
        record = writer.write_proposal(tmp_path, model)
        approved = json.loads(record.read_text(encoding="utf-8"))
        approved["status"] = "approved"
        approved["decision_artifact_sha256"] = approved["artifact_sha256"]
        record.write_text(json.dumps(approved), encoding="utf-8")

        writer.write_proposal(tmp_path, model)

        assert json.loads(record.read_text(encoding="utf-8"))["status"] == "approved"

    def test_changed_model_requires_a_new_visual_decision(self, tmp_path) -> None:
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        model.parent.mkdir(parents=True)
        self._write_model(model, 10.0)
        writer = FabricationAssemblyReviewRecord()
        record = writer.write_proposal(tmp_path, model)
        approved = json.loads(record.read_text(encoding="utf-8"))
        approved["status"] = "approved"
        approved["decision_artifact_sha256"] = approved["artifact_sha256"]
        record.write_text(json.dumps(approved), encoding="utf-8")
        self._write_model(model, 20.0)

        writer.write_proposal(tmp_path, model)

        saved = json.loads(record.read_text(encoding="utf-8"))
        assert saved["status"] == "proposed"
        assert saved["artifact"] == "assemblies/full_wardrobe_review.glb"

    def _write_model(self, path, size) -> None:
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


__all__ = ["TestFabricationAssemblyReviewRecord"]
