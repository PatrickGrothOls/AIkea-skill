"""Scope: Assign an independent review state to each cabinet door in a wardrobe."""

from __future__ import annotations

from dataclasses import dataclass

from door_review_state import DoorReviewState


class DoorReviewPlanError(ValueError):
    """Report an invalid cabinet-specific door review assignment."""


@dataclass(frozen=True)
class FullWardrobeDoorPlan:
    """Resolve default and cabinet-specific door states for one review export."""

    default_state: DoorReviewState
    assignments: tuple[tuple[str, DoorReviewState], ...] = ()

    @classmethod
    def uniform(cls, state: DoorReviewState) -> FullWardrobeDoorPlan:
        return cls(state)

    @classmethod
    def from_assignments(
        cls,
        default_state: DoorReviewState,
        assignments: tuple[str, ...],
    ) -> FullWardrobeDoorPlan:
        parsed: list[tuple[str, DoorReviewState]] = []
        seen: set[str] = set()
        for assignment in assignments:
            assembly_id, separator, value = assignment.partition("=")
            if not separator or not assembly_id or not value:
                raise DoorReviewPlanError(
                    "door state must use <assembly-id>=<closed|open|removed>"
                )
            if assembly_id in seen:
                raise DoorReviewPlanError(
                    f"door state supplied more than once for {assembly_id}"
                )
            try:
                state = DoorReviewState(value)
            except ValueError as error:
                raise DoorReviewPlanError(
                    f"unsupported door state for {assembly_id}: {value}"
                ) from error
            parsed.append((assembly_id, state))
            seen.add(assembly_id)
        return cls(default_state, tuple(parsed))

    def states_for(
        self,
        assembly_ids: tuple[str, ...],
    ) -> dict[str, DoorReviewState]:
        states = {assembly_id: self.default_state for assembly_id in assembly_ids}
        states.update(self.assignments)
        return states

    def unknown_assembly_ids(
        self,
        assembly_ids: tuple[str, ...],
    ) -> tuple[str, ...]:
        known = set(assembly_ids)
        return tuple(
            assembly_id
            for assembly_id, _state in self.assignments
            if assembly_id not in known
        )

    def filename_for(self, assembly_ids: tuple[str, ...]) -> str:
        states = set(self.states_for(assembly_ids).values())
        if states == {DoorReviewState.CLOSED}:
            return "full_wardrobe_review.glb"
        if states == {DoorReviewState.OPEN}:
            return "full_wardrobe_open_review.glb"
        if states == {DoorReviewState.REMOVED}:
            return "full_wardrobe_doors_removed_review.glb"
        return "full_wardrobe_door_states_review.glb"


__all__ = ["DoorReviewPlanError", "FullWardrobeDoorPlan"]
