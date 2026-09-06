"""Scope: Verify the two-state KA 4532 proof orchestration contract."""

import json

import pytest

from hettich_ka_4532_spacer_proof_generator import (
    HettichKa4532SpacerProofGenerator,
)
from hettich_ka_4532_spacer_proof_generator_test_support import (
    CompleteReviewProbe,
    HettichKa4532SpacerProofProjectFixture,
    ProofCheckerProbe,
    StepLoaderProbe,
)


class TestHettichKa4532SpacerProofGenerator:
    """Keep exact proof generation on the generic recursive review path."""

    def test_compares_closed_and_open_with_the_same_door_state(self, tmp_path) -> None:
        HettichKa4532SpacerProofProjectFixture().write(tmp_path)
        review = CompleteReviewProbe()
        checker = ProofCheckerProbe()
        generator = HettichKa4532SpacerProofGenerator(
            review,
            checker,
            StepLoaderProbe(),
        )

        result = generator.generate(
            tmp_path,
            "cabinet_01",
            tmp_path / "review",
            {"cabinet_01/door_hinges": "open"},
        )

        assert [call[3] for call in review.calls] == [
            {"cabinet_01/door_hinges": "open", "cabinet_01/drawers": "closed"},
            {"cabinet_01/door_hinges": "open", "cabinet_01/drawers": "open"},
        ]
        assert checker.call[3] == ("closed",)
        assert checker.call[4] == ("open",)
        assert checker.call[6] == "exact-step-set"
        assert len(checker.call[9]) == 2
        assert result.report_path.is_file()

    def test_failed_rerun_invalidates_older_valid_evidence(self, tmp_path) -> None:
        HettichKa4532SpacerProofProjectFixture().write(tmp_path)
        generator = HettichKa4532SpacerProofGenerator(
            CompleteReviewProbe(),
            ProofCheckerProbe(),
            StepLoaderProbe(),
        )
        output = tmp_path / "review"
        generator.generate(tmp_path, "cabinet_01", output)

        with pytest.raises(ValueError, match="proof owns drawer feature state"):
            generator.generate(
                tmp_path,
                "cabinet_01",
                output,
                {"cabinet_01/drawers": "removed"},
            )

        evidence = json.loads(
            (output / "ka4532-spacer-movement-collision-check.json").read_text()
        )
        assert evidence["status"] == "invalidated-before-run"
        assert evidence["manufacturing_authority"] is False
