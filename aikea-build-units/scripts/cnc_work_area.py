"""Scope: Resolve the usable rectangular cutting area for one CNC profile."""

from __future__ import annotations

from dataclasses import dataclass


class CncWorkAreaError(ValueError):
    """Report a part dimension that cannot enter the configured CNC area."""


@dataclass(frozen=True)
class CncWorkArea:
    """Keep machine travel and cutter-radius clearance in one profile."""

    profile_id: str
    x_travel_mm: float
    y_travel_mm: float
    cutter_diameter_mm: float

    def __post_init__(self) -> None:
        values = (self.x_travel_mm, self.y_travel_mm, self.cutter_diameter_mm)
        if any(value <= 0 for value in values):
            raise ValueError("CNC travel and cutter diameter must be greater than zero")
        if self.cutter_radius_mm >= min(self.x_travel_mm, self.y_travel_mm):
            raise ValueError("cutter radius must be smaller than both CNC axes")

    @property
    def cutter_radius_mm(self) -> float:
        return self.cutter_diameter_mm / 2.0

    @property
    def usable_x_mm(self) -> float:
        return self.x_travel_mm - self.cutter_radius_mm

    @property
    def usable_y_mm(self) -> float:
        return self.y_travel_mm - self.cutter_radius_mm

    def fits(self, width_mm: float, height_mm: float) -> bool:
        return (
            width_mm <= self.usable_x_mm and height_mm <= self.usable_y_mm
        ) or (
            width_mm <= self.usable_y_mm and height_mm <= self.usable_x_mm
        )

    def maximum_span_mm(self, transverse_size_mm: float) -> float:
        candidates = []
        if transverse_size_mm <= self.usable_y_mm:
            candidates.append(self.usable_x_mm)
        if transverse_size_mm <= self.usable_x_mm:
            candidates.append(self.usable_y_mm)
        if not candidates:
            raise CncWorkAreaError(
                f"{transverse_size_mm:g} mm exceeds both usable CNC axes"
            )
        return max(candidates)


CNC_2500_X_2000_8MM = CncWorkArea(
    profile_id="cnc-2500x2000-8mm",
    x_travel_mm=2500.0,
    y_travel_mm=2000.0,
    cutter_diameter_mm=8.0,
)


__all__ = ["CNC_2500_X_2000_8MM", "CncWorkArea", "CncWorkAreaError"]
