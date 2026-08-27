"""Scope: Build already-generated cabinet parts in a selected review pose."""

from __future__ import annotations

from typing import Any

from assembly_part_locator import AssemblyPartLocator
from cabinet_assembly_geometry import CabinetAssemblyGeometry
from door_review_pose import DoorReviewPose
from review_part_locator import ReviewPartLocator
from unit_mockup import MockupPart


class CabinetReviewGeometry:
    """Choose physical or open-door placement for one built cabinet."""

    def __init__(self) -> None:
        self.closed_geometry = CabinetAssemblyGeometry(AssemblyPartLocator())
        self.open_geometry = CabinetAssemblyGeometry(ReviewPartLocator())

    def build(
        self,
        built_assembly: Any,
        door_pose: DoorReviewPose,
    ) -> tuple[MockupPart, ...]:
        geometry = {
            DoorReviewPose.CLOSED: self.closed_geometry,
            DoorReviewPose.OPEN: self.open_geometry,
        }[door_pose]
        return geometry.build(built_assembly)


__all__ = ["CabinetReviewGeometry"]
