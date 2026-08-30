"""Scope: Generate exact horizontal extrema and conservative top samples for one door sweep."""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, radians, sin
from typing import Any, Iterator

from door_hinge_side import DoorHingeSide
from door_top_profile import DoorTopProfile


@dataclass(frozen=True, slots=True)
class DoorSweepTopSample:
    x_mm: float
    height_mm: float


class DoorOpeningSweep:
    """Own one door's movement independently of the room being checked."""

    REQUIRED_ANGLE_DEGREES = 90.0
    ANGLE_STEP_DEGREES = 0.25
    TOP_STEP_MM = 2.0

    def __init__(
        self,
        assembly: Any,
        door: Any,
        pivot: tuple[float, float],
        hinge_side: DoorHingeSide,
    ) -> None:
        self.assembly = assembly
        self.dimensions = {
            name: float(value) for name, value in door.dimensions_mm
        }
        self.pivot = pivot
        self.top = DoorTopProfile.from_part(door)
        angle = radians(self.REQUIRED_ANGLE_DEGREES)
        self.angle_bounds = (
            (0.0, -angle)
            if hinge_side is DoorHingeSide.LEFT
            else (0.0, angle)
        )
        self.edge_gap_mm = (
            float(assembly.width_mm) - self.dimensions["width"]
        ) / 2.0

    @property
    def horizontal_extent_mm(self) -> tuple[float, float]:
        x_values = tuple(
            float(self.assembly.global_left_mm)
            + self._rotated_x(point, angle)
            for point in self._footprint_corners()
            for angle in self._extreme_angles(point)
        )
        return min(x_values), max(x_values)

    @property
    def maximum_radius_mm(self) -> float:
        return max(
            hypot(x_mm - self.pivot[0], y_mm - self.pivot[1])
            for x_mm, y_mm in self._footprint_corners()
        )

    @property
    def angular_half_step_radians(self) -> float:
        return radians(self.ANGLE_STEP_DEGREES / 2.0)

    @property
    def top_half_step_mm(self) -> float:
        return self.TOP_STEP_MM / 2.0

    def top_samples(self) -> Iterator[DoorSweepTopSample]:
        for angle in self._sampled_angles():
            for point in self.top.samples(self.TOP_STEP_MM):
                for y_mm in (0.0, -self.dimensions["thickness"]):
                    yield DoorSweepTopSample(
                        float(self.assembly.global_left_mm)
                        + self._rotated_x(
                            (self.edge_gap_mm + point.x_mm, y_mm), angle
                        ),
                        float(self.assembly.door_bottom_mm) + point.height_mm,
                    )

    def _footprint_corners(self) -> tuple[tuple[float, float], ...]:
        return tuple(
            (x_mm, y_mm)
            for x_mm in (
                self.edge_gap_mm,
                self.edge_gap_mm + self.dimensions["width"],
            )
            for y_mm in (0.0, -self.dimensions["thickness"])
        )

    def _extreme_angles(
        self,
        point: tuple[float, float],
    ) -> tuple[float, ...]:
        low, high = sorted(self.angle_bounds)
        dx, dy = point[0] - self.pivot[0], point[1] - self.pivot[1]
        base = atan2(-dy, dx)
        candidates = [low, high]
        candidates.extend(base + offset * pi for offset in range(-2, 3))
        return tuple(angle for angle in candidates if low <= angle <= high)

    def _sampled_angles(self) -> tuple[float, ...]:
        count = round(self.REQUIRED_ANGLE_DEGREES / self.ANGLE_STEP_DEGREES)
        start, end = self.angle_bounds
        return tuple(
            start + (end - start) * index / count for index in range(count + 1)
        )

    def _rotated_x(self, point: tuple[float, float], angle: float) -> float:
        dx, dy = point[0] - self.pivot[0], point[1] - self.pivot[1]
        return self.pivot[0] + dx * cos(angle) - dy * sin(angle)


__all__ = ["DoorOpeningSweep", "DoorSweepTopSample"]
