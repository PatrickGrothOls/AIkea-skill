"""Scope: Name the supported visual poses for one built drawer child."""

from enum import Enum


class DrawerReviewState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"


__all__ = ["DrawerReviewState"]
