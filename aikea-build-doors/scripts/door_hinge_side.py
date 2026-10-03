"""Scope: Name the cabinet side that owns a single door's concealed hinges."""

from __future__ import annotations

from enum import Enum


class DoorHingeSide(str, Enum):
    """Map a client-visible hinge hand to its generated cabinet features."""

    LEFT = "left"
    RIGHT = "right"

    @property
    def side_part_id(self) -> str:
        return f"{self.value}_side"

    @property
    def door_height_dimension(self) -> str:
        return f"{self.value}_height"

    def opening_angle_degrees(self, left_open_angle_degrees: float) -> float:
        return (
            left_open_angle_degrees
            if self is DoorHingeSide.LEFT
            else -left_open_angle_degrees
        )


__all__ = ["DoorHingeSide"]
