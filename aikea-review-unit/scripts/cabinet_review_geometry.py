"""Scope: Build already-generated cabinet parts in a selected review pose."""

from __future__ import annotations

from typing import Any

from assembly_part_locator import AssemblyPartLocator
from cabinet_assembly_geometry import CabinetAssemblyGeometry
from door_review_state import DoorReviewState
from review_part_locator import ReviewPartLocator
from unit_mockup import MockupPart


class CabinetReviewGeometry:
    """Choose closed, open, or door-removed presentation for one cabinet."""

    def __init__(self) -> None:
        self.closed_geometry = CabinetAssemblyGeometry(AssemblyPartLocator())
        self.open_geometry = CabinetAssemblyGeometry(ReviewPartLocator())

    def build(
        self,
        built_assembly: Any,
        door_state: DoorReviewState,
    ) -> tuple[MockupPart, ...]:
        if door_state is DoorReviewState.REMOVED:
            return tuple(
                part
                for part in self.closed_geometry.build(built_assembly)
                if part.name != "door_panel"
            )
        geometry = {
            DoorReviewState.CLOSED: self.closed_geometry,
            DoorReviewState.OPEN: self.open_geometry,
        }[door_state]
        return geometry.build(built_assembly)


__all__ = ["CabinetReviewGeometry"]
