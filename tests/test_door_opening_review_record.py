"""Scope: Verify the visual approval record represents the complete door run."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from door_hinge_side import DoorHingeSide
from door_opening_review_record import DoorOpeningReviewRecord
from door_opening_side_resolver import DoorOpeningSidePlan


class TestDoorOpeningReviewRecord(unittest.TestCase):
    def test_proposal_lists_every_door_and_marks_only_real_exceptions(self) -> None:
        plans = (
            self._plan("tall_storage_01", DoorHingeSide.LEFT),
            self._plan("tall_storage_02", DoorHingeSide.RIGHT, "client_choice"),
            self._plan("tall_storage_03", DoorHingeSide.LEFT),
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / "reviews/door-openings.json"

            DoorOpeningReviewRecord().write_proposal(path, plans)

            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved["status"], "proposed")
            self.assertEqual([door["assembly_id"] for door in saved["doors"]], [
                "tall_storage_01",
                "tall_storage_02",
                "tall_storage_03",
            ])
            self.assertEqual([door["label"] for door in saved["doors"]], [
                "Cabinet 1",
                "Cabinet 2",
                "Cabinet 3",
            ])
            self.assertFalse(saved["doors"][0]["exception"])
            self.assertTrue(saved["doors"][1]["exception"])
            self.assertEqual(saved["doors"][1]["note"], "your requested opening")
            self.assertNotIn("opens_90_degrees", saved["doors"][0])

    def _plan(
        self,
        assembly_id: str,
        side: DoorHingeSide,
        source: str = "standard",
    ) -> DoorOpeningSidePlan:
        return DoorOpeningSidePlan(
            assembly_id,
            DoorHingeSide.LEFT,
            side,
            "resolved opening hand",
            source,
        )


if __name__ == "__main__":
    unittest.main()
