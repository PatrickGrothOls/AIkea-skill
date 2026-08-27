"""Scope: Name the supported door poses for cabinet visual review."""

from enum import Enum


class DoorReviewPose(str, Enum):
    """Select how unchanged door parts appear in a review model."""

    CLOSED = "closed"
    OPEN = "open"


__all__ = ["DoorReviewPose"]
