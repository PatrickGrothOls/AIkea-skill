"""Scope: Verify only canonical closed wardrobe output creates a proposal."""

from __future__ import annotations

from types import SimpleNamespace

from fabrication_review_proposal_writer import FabricationReviewProposalWriter


class RecordProbe:
    """Capture proposal writes without depending on GLB parsing."""

    def __init__(self) -> None:
        self.call = None

    def write_proposal(self, project_root, model_path):
        self.call = project_root, model_path
        return project_root / "reviews/fabrication-assembly.json"


class TestFabricationReviewProposalWriter:
    """Keep proposal persistence at the explicit application workflow boundary."""

    def test_writes_for_the_canonical_closed_result(self, tmp_path) -> None:
        records = RecordProbe()
        model = tmp_path / "assemblies/full_wardrobe_review.glb"
        result = SimpleNamespace(
            glb_path=model,
            door_states={"cabinet_01": "closed"},
        )

        path = FabricationReviewProposalWriter(records).write_for_result(
            tmp_path,
            result,
        )

        assert path == tmp_path / "reviews/fabrication-assembly.json"
        assert records.call == (tmp_path, model)

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
