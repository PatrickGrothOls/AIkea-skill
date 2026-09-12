"""Scope: Verify only canonical closed wardrobe output creates a proposal."""

from __future__ import annotations

from types import SimpleNamespace
import json

from fabrication_review_proposal_writer import FabricationReviewProposalWriter


class RecordProbe:
    """Capture proposal writes without depending on GLB parsing."""

    def __init__(self) -> None:
        self.call = None

    def write_proposal(self, project_root, model_path, construction_sha256):
        self.call = project_root, model_path, construction_sha256
        return project_root / "reviews/fabrication-assembly.json"


class TestFabricationReviewProposalWriter:
    """Keep proposal persistence at the explicit application workflow boundary."""

    def test_writes_for_the_canonical_closed_result(self, tmp_path) -> None:
        records = RecordProbe()
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        result = SimpleNamespace(
            glb_path=model,
            door_states={"cabinet_01": "closed"},
            construction_sha256="current-inputs",
            construction_position_status="valid",
        )

        evidence = tmp_path / "assemblies/construction-position-check.json"
        evidence.parent.mkdir(parents=True)
        evidence.write_text(json.dumps({"schema_version": 2, "status": "valid",
                                        "construction_sha256": "current-inputs"}))
        path = FabricationReviewProposalWriter(records).write_for_result(
            tmp_path,
            result,
        )

        assert path == tmp_path / "reviews/fabrication-assembly.json"
        assert records.call == (tmp_path, model, "current-inputs")

    def test_skips_open_or_noncanonical_results(self, tmp_path) -> None:
        records = RecordProbe()
        writer = FabricationReviewProposalWriter(records)
        results = (
            SimpleNamespace(
                glb_path=tmp_path / "assemblies/full_wardrobe_review.glb",
                door_states={"cabinet_01": "open"},
            ),
            SimpleNamespace(
                glb_path=tmp_path / "assemblies/custom_review.glb",
                door_states={"cabinet_01": "closed"},
            ),
        )

        assert tuple(writer.write_for_result(tmp_path, item) for item in results) == (
            None,
            None,
        )
        assert records.call is None


__all__ = ["TestFabricationReviewProposalWriter"]
