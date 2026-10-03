"""Scope: Define useful hinge-center spread inside one door panel."""

from __future__ import annotations


class DoorHingeSpreadPolicy:
    """Provide ideal centers and enforce the door-edge working margin."""

    _EDGE_MARGIN_MM = 100.0

    def ideal_centers_mm(
        self,
        door_height_mm: float,
        hinge_count: int,
    ) -> tuple[float, ...]:
        span_mm = door_height_mm - 2.0 * self._EDGE_MARGIN_MM
        return tuple(
            self._EDGE_MARGIN_MM + span_mm * index / (hinge_count - 1)
            for index in range(hinge_count)
        )

    def contains(self, center_mm: float, door_height_mm: float) -> bool:
        return (
            self._EDGE_MARGIN_MM
            <= center_mm
            <= door_height_mm - self._EDGE_MARGIN_MM
        )


__all__ = ["DoorHingeSpreadPolicy"]
