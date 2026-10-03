"""Scope: Place built drawer children without moving cabinet-owned hardware."""

from __future__ import annotations

from typing import Any

from drawer_review_motion import DrawerReviewMotion
from drawer_review_state import DrawerReviewState
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart, UnitMockupInputError


class DrawerReviewGeometry:
    """Apply review motion only to a drawer child and its owned box parts."""

    _DRAWER_COLOR = (0.84, 0.75, 0.62, 1.0)

    def __init__(self) -> None:
        self.frame_location = LocalToParentLocation()
        self.review_motion = DrawerReviewMotion()

    def build(
        self,
        built_cabinet: Any,
        state: DrawerReviewState,
    ) -> tuple[MockupPart, ...]:
        drawers = tuple(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )
        if len(drawers) != 1:
            raise UnitMockupInputError(
                ["drawer review requires exactly one built drawer child"]
            )
        child = drawers[0]
        if state is DrawerReviewState.REMOVED:
            return ()
        box = child.assembly.spec.box
        child_location = self.frame_location.build(child.spec.local_to_parent)
        pose = self.review_motion.location(state, box.side_length_mm)
        return tuple(
            MockupPart(
                f"{child.spec.assembly_id}__{part.spec.part_id}",
                part.solid,
                child_location
                * pose
                * self.frame_location.build(part.spec.local_to_parent),
                self._DRAWER_COLOR,
            )
            for part in child.assembly.parts
        )

__all__ = ["DrawerReviewGeometry"]
