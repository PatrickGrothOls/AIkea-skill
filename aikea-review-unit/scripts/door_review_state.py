"""Scope: Name whether one cabinet door is closed, open, or absent from a review."""

from enum import Enum


class DoorReviewState(str, Enum):
    """Select how one unchanged door part appears in a review model."""

    CLOSED = "closed"
    OPEN = "open"
    REMOVED = "removed"


__all__ = ["DoorReviewState"]
