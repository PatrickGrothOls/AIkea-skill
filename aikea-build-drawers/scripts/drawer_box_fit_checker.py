"""Scope: Verify drawer sheets meet exactly without occupying the same material."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from drawer_box_builder import BuiltDrawerBox

PartPair = tuple[str, str]


@dataclass(frozen=True, slots=True)
class DrawerBoxFitReport:
    """Describe missing contacts and unintended material overlaps."""

    intended_contacts: tuple[PartPair, ...]
    missing_contacts: tuple[PartPair, ...]
    overlapping_parts: tuple[PartPair, ...]

    @property
    def passed(self) -> bool:
        return not self.missing_contacts and not self.overlapping_parts


class DrawerBoxFitChecker:
    """Check the physical relationships expected from an unmachined box."""

    _INTENDED_CONTACTS: tuple[PartPair, ...] = (
        ("left_side", "front"),
        ("left_side", "back"),
        ("left_side", "bottom"),
        ("right_side", "front"),
        ("right_side", "back"),
        ("right_side", "bottom"),
        ("front", "bottom"),
        ("back", "bottom"),
    )

    def check(self, drawer: BuiltDrawerBox) -> DrawerBoxFitReport:
        shapes = {
            part.spec.part_id: part.placed_shape()
            for part in drawer.parts
        }
        missing = tuple(
            pair
            for pair in self._INTENDED_CONTACTS
            if shapes[pair[0]].distance(shapes[pair[1]]) > 1e-6
        )
        overlapping = tuple(
            (left_id, right_id)
            for left_id, right_id in combinations(shapes, 2)
            if shapes[left_id].intersect(shapes[right_id]).Volume() > 1e-6
        )
        return DrawerBoxFitReport(
            intended_contacts=self._INTENDED_CONTACTS,
            missing_contacts=missing,
            overlapping_parts=overlapping,
        )


__all__ = ["DrawerBoxFitChecker", "DrawerBoxFitReport", "PartPair"]
