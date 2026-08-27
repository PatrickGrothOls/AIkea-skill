"""Scope: Calculate the physical bottom height of a selected door design."""

from __future__ import annotations

from door_and_plinth_settings import DoorBottom


class DoorBottomHeightResolver:
    """Map the shared door choice to one local assembly height."""

    def resolve(
        self,
        choice: DoorBottom,
        base_height_mm: float,
        deck_thickness_mm: float,
    ) -> float:
        if choice is DoorBottom.FLOOR:
            return 0.0
        bottom_mm = base_height_mm - deck_thickness_mm
        if bottom_mm <= 0.0:
            raise ValueError("base height must leave a positive plinth below the deck")
        return bottom_mm


__all__ = ["DoorBottomHeightResolver"]
