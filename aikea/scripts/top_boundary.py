"""Scope: Resolve a flat or explicitly shaped top boundary from site readings."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from height_measurements import HeightMeasurement, HeightMeasurementReader


class TopBoundaryKind(str, Enum):
    """Name how measured heights affect the wardrobe top."""

    FLAT = "flat"
    MEASURED_PROFILE = "measured_profile"


@dataclass(frozen=True)
class TopBoundary:
    """Provide safe heights for one confirmed top-boundary kind."""

    kind: TopBoundaryKind
    measurements: tuple[HeightMeasurement, ...]

    @property
    def minimum_height_mm(self) -> float:
        return min(item.height_from_floor_mm for item in self.measurements)

    def height_at(self, position_mm: float) -> float:
        if self.kind is TopBoundaryKind.FLAT or len(self.measurements) == 1:
            return self.minimum_height_mm
        for left, right in zip(self.measurements, self.measurements[1:]):
            if left.distance_from_left_mm <= position_mm <= right.distance_from_left_mm:
                run = right.distance_from_left_mm - left.distance_from_left_mm
                fraction = (position_mm - left.distance_from_left_mm) / run
                rise = right.height_from_floor_mm - left.height_from_floor_mm
                return left.height_from_floor_mm + rise * fraction
        raise ValueError(f"no top-boundary measurement covers {position_mm} mm")


class TopBoundaryReader:
    """Read the confirmed top shape and its raw height measurements."""

    def read(
        self,
        measured_space: dict[str, Any],
        required_width_mm: float,
        is_fitted: bool,
        scale: float,
        problems: list[str],
    ) -> TopBoundary:
        raw_kind = measured_space.get("top_boundary")
        try:
            kind = TopBoundaryKind(raw_kind)
        except ValueError:
            problems.append(
                "measured_space.top_boundary must be 'flat' or 'measured_profile'"
            )
            kind = TopBoundaryKind.FLAT
        measurements = HeightMeasurementReader().read(
            measured_space.get("height_measurements"),
            required_width_mm,
            is_fitted,
            scale,
            problems,
        )
        return TopBoundary(kind, measurements)
