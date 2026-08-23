"""Scope: Represent and serialize calculated overall wardrobe dimensions."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CabinetOverallSize:
    cabinet_number: int
    left_position_mm: float
    right_position_mm: float
    width_mm: float
    left_height_mm: float
    right_height_mm: float
    door_width_mm: float


@dataclass(frozen=True)
class OverallWardrobeResult:
    minimum_measured_width_mm: float
    minimum_measured_depth_mm: float
    width_fitting_allowance_mm: float
    depth_fitting_allowance_mm: float
    height_fitting_allowance_mm: float
    usable_width_mm: float
    usable_depth_mm: float
    cabinet_depth_mm: float
    inside_depth_mm: float
    cabinets: tuple[CabinetOverallSize, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "minimum_measured_width_mm": self.minimum_measured_width_mm,
            "minimum_measured_depth_mm": self.minimum_measured_depth_mm,
            "width_fitting_allowance_mm": self.width_fitting_allowance_mm,
            "depth_fitting_allowance_mm": self.depth_fitting_allowance_mm,
            "height_fitting_allowance_mm": self.height_fitting_allowance_mm,
            "usable_width_mm": self.usable_width_mm,
            "usable_depth_mm": self.usable_depth_mm,
            "cabinet_depth_mm": self.cabinet_depth_mm,
            "inside_depth_mm": self.inside_depth_mm,
            "cabinets": [asdict(cabinet) for cabinet in self.cabinets],
        }
