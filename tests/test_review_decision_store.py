"""Scope: Verify door-opening approval is persisted by the local review boundary."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from review_decision_store import ReviewDecisionStore


class TestReviewDecisionStore(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.path = Path(self.temporary_directory.name) / "opening-review.json"
        self.path.write_text(
            json.dumps(
                {
                    "review_type": "door_openings",
                    "status": "proposed",
                    "message": "All single doors hinge on the left unless marked otherwise.",
                    "doors": [
                        {
                            "assembly_id": "tall_storage_01",
                            "hinge_side": "left",
                            "exception": False,
                            "opens_90_degrees": True,
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

    def test_approval_confirms_the_proposed_local_opening(self) -> None:
        result = ReviewDecisionStore(self.path).decide("approved")

        self.assertEqual(result["status"], "approved")
        self.assertIn("decided_at", result)
        saved = json.loads(self.path.read_text(encoding="utf-8"))
        self.assertEqual(saved["doors"][0]["hinge_side"], "left")

    def test_change_request_keeps_the_proposal_available_for_revision(self) -> None:
        result = ReviewDecisionStore(self.path).decide("change_requested")

        self.assertEqual(result["status"], "change_requested")
        self.assertEqual(result["doors"][0]["assembly_id"], "tall_storage_01")

    def test_unknown_decision_is_rejected_without_changing_the_record(self) -> None:
        before = self.path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "unsupported"):
            ReviewDecisionStore(self.path).decide("maybe")

        self.assertEqual(self.path.read_text(encoding="utf-8"), before)

    def test_accepts_a_fabrication_assembly_decision(self) -> None:
        self.path.write_text(
            json.dumps(
                {
                    "review_type": "fabrication_assembly",
                    "status": "proposed",
                    "message": "Approve this exact assembly.",
                    "artifact_sha256": "abc123",
                }
            ),
            encoding="utf-8",
        )

        result = ReviewDecisionStore(self.path).decide("approved")

        self.assertEqual(result["status"], "approved")
        self.assertEqual(result["artifact_sha256"], "abc123")


if __name__ == "__main__":
    unittest.main()
