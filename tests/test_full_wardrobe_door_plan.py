"""Scope: Verify independent door-state planning for full wardrobe reviews."""

import pytest

from door_review_state import DoorReviewState
from full_wardrobe_door_plan import FullWardrobeDoorPlan


class TestFullWardrobeDoorPlan:
    """Protect parsing, module selection, and review artifact naming."""

    def test_applies_independent_states_and_keeps_unspecified_modules_closed(self) -> None:
        plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            ("tall_storage_01=open", "tall_storage_02=removed"),
        )

        assert plan.states_for(
            ("tall_storage_01", "tall_storage_02", "tall_storage_03")
        ) == {
            "tall_storage_01": DoorReviewState.OPEN,
            "tall_storage_02": DoorReviewState.REMOVED,
            "tall_storage_03": DoorReviewState.CLOSED,
        }

    def test_names_uniform_and_independent_review_artifacts(self) -> None:
        assembly_ids = ("tall_storage_01", "tall_storage_02", "tall_storage_03")

        assert FullWardrobeDoorPlan.uniform(DoorReviewState.CLOSED).filename_for(
            assembly_ids
        ) == "full_wardrobe_review.glb"
        assert FullWardrobeDoorPlan.uniform(DoorReviewState.OPEN).filename_for(
            assembly_ids
        ) == "full_wardrobe_open_review.glb"
        assert FullWardrobeDoorPlan.uniform(DoorReviewState.REMOVED).filename_for(
            assembly_ids
        ) == "full_wardrobe_doors_removed_review.glb"
        assert FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            ("tall_storage_01=open",),
        ).filename_for(assembly_ids) == "full_wardrobe_door_states_review.glb"

    def test_rejects_duplicate_and_unknown_module_assignments(self) -> None:
        with pytest.raises(ValueError, match="more than once"):
            FullWardrobeDoorPlan.from_assignments(
                DoorReviewState.CLOSED,
                ("tall_storage_01=open", "tall_storage_01=removed"),
            )

        plan = FullWardrobeDoorPlan.from_assignments(
            DoorReviewState.CLOSED,
            ("missing=open",),
        )
        assert plan.unknown_assembly_ids(("tall_storage_01",)) == ("missing",)
