"""Scope: Define fixed Cabineo construction profiles owned by AIkea."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class CabineoProfile:
    """Own the measured machining dimensions of one connector relationship."""

    profile_id: str
    profile_revision: int
    pocket_radius_mm: float
    pocket_join_half_width_mm: float
    pocket_rear_center_mm: float
    pocket_depth_mm: float
    receiver_diameter_mm: float
    receiver_depth_mm: float
    receiver_axis_height_mm: float
    minimum_sheet_thickness_mm: float

    @property
    def pocket_centers_mm(self) -> tuple[float, float, float]:
        pitch = 2 * sqrt(
            self.pocket_radius_mm**2 - self.pocket_join_half_width_mm**2
        )
        rear = self.pocket_rear_center_mm
        return rear - 2 * pitch, rear - pitch, rear


NON_BOTTOM_CABINEO = CabineoProfile(
    profile_id="cabineo_8_non_bottom",
    profile_revision=2,
    pocket_radius_mm=7.5,
    pocket_join_half_width_mm=5.0,
    pocket_rear_center_mm=25.5,
    pocket_depth_mm=10.5,
    receiver_diameter_mm=9.1,
    receiver_depth_mm=12.5,
    receiver_axis_height_mm=5.0,
    minimum_sheet_thickness_mm=10.0,
)


__all__ = ["CabineoProfile", "NON_BOTTOM_CABINEO"]
