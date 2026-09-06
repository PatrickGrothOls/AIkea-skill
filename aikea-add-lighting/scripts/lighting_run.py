"""Scope: Define one saved straight lighting run in its owning part's plane."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, degrees, hypot

from recessed_luminaire_profile import RecessedLuminaireProfile

Point2D = tuple[float, float]


@dataclass(frozen=True, slots=True)
class LightingRun:
    """Own the placement shared by machining, hardware, and emitted light."""

    run_id: str
    start_mm: Point2D
    end_mm: Point2D
    color_temperature_k: int
    profile: RecessedLuminaireProfile

    def __post_init__(self) -> None:
        if self.length_mm <= 0:
            raise ValueError("a lighting run needs two different endpoints")
        if not self.profile.supports(self.color_temperature_k):
            raise ValueError(
                f"{self.profile.product_name} does not offer "
                f"{self.color_temperature_k} K"
            )

    @property
    def length_mm(self) -> float:
        return hypot(
            self.end_mm[0] - self.start_mm[0],
            self.end_mm[1] - self.start_mm[1],
        )

    @property
    def angle_degrees(self) -> float:
        return degrees(
            atan2(
                self.end_mm[1] - self.start_mm[1],
                self.end_mm[0] - self.start_mm[0],
            )
        )

    def as_record(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "host_plane": "part-face-local XY; positive Z points out of the sheet",
            "start_mm": list(self.start_mm),
            "end_mm": list(self.end_mm),
            "length_mm": self.length_mm,
            "color_temperature_k": self.color_temperature_k,
            "purchased_luminaire": {
                "profile_id": self.profile.profile_id,
                "manufacturer": self.profile.manufacturer,
                "product_name": self.profile.product_name,
                "source_url": self.profile.source_url,
                "groove_width_mm": self.profile.groove_width_mm,
                "groove_depth_mm": self.profile.groove_depth_mm,
            },
        }


__all__ = ["LightingRun", "Point2D"]
