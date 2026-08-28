"""Scope: Place built drawer children without moving cabinet-owned hardware."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from drawer_part_locator import DrawerPartLocator
from drawer_review_state import DrawerReviewState
from local_to_parent_location import LocalToParentLocation
from unit_mockup import MockupPart, UnitMockupInputError


class DrawerReviewGeometry:
    """Apply review motion only to a drawer child and its owned box parts."""

    _DRAWER_COLOR = (0.84, 0.75, 0.62, 1.0)
    _OPEN_FRACTION = 0.75

    def __init__(self) -> None:
        self.part_locator = DrawerPartLocator()
        self.frame_location = LocalToParentLocation()

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
        box = child.assembly.spec.box
        child_location = self.frame_location.build(child.spec.local_to_parent)
        pose = self._pose(state, box.side_length_mm)
        return tuple(
            MockupPart(
                f"{child.spec.assembly_id}__{part.spec.part_id}",
                part.solid,
                child_location
                * pose
                * self.part_locator.placement(part.spec.part_id, box).location(),
                self._DRAWER_COLOR,
            )
            for part in child.assembly.parts
        )

    def _pose(self, state: DrawerReviewState, side_length_mm: float) -> cq.Location:
        extension_mm = (
            side_length_mm * self._OPEN_FRACTION
            if state is DrawerReviewState.OPEN
            else 0.0
        )
        return cq.Location(cq.Vector(0.0, -extension_mm, 0.0))


__all__ = ["DrawerReviewGeometry"]
