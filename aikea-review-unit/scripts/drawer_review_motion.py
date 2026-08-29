"""Scope: Resolve the one visual motion shared by a drawer and its hardware."""

from __future__ import annotations

import cadquery as cq

from drawer_review_state import DrawerReviewState


class DrawerReviewMotion:
    """Keep review-only drawer travel out of physical mounting frames."""

    _OPEN_FRACTION = 0.75

    def location(
        self,
        state: DrawerReviewState,
        side_length_mm: float,
    ) -> cq.Location:
        extension_mm = self.extension_mm(state, side_length_mm)
        return cq.Location(cq.Vector(0.0, -extension_mm, 0.0))

    def extension_mm(
        self,
        state: DrawerReviewState,
        side_length_mm: float,
    ) -> float:
        return (
            side_length_mm * self._OPEN_FRACTION
            if state is DrawerReviewState.OPEN
            else 0.0
        )


__all__ = ["DrawerReviewMotion"]
