"""Scope: Read and validate the measured ceiling points from left to right."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class CeilingPoint:
    distance_from_left_mm: float
    height_from_floor_mm: float


class CeilingPointReader:
    """Turn editable ceiling points into checked millimetre values."""

    def read(
        self,
        raw_points: Any,
        width_mm: float,
        scale: float,
        problems: list[str],
    ) -> tuple[CeilingPoint, ...]:
        if not isinstance(raw_points, list) or len(raw_points) < 2:
            problems.append("measured_space.ceiling_points must contain at least two points")
            return ()
        points: list[CeilingPoint] = []
        for index, raw in enumerate(raw_points):
            if not isinstance(raw, dict):
                problems.append(f"measured_space.ceiling_points[{index}] must be an object")
                continue
            distance = raw.get("distance_from_left")
            height = raw.get("height_from_floor")
            if any(
                isinstance(value, bool) or not isinstance(value, (int, float))
                for value in (distance, height)
            ):
                problems.append(
                    f"measured_space.ceiling_points[{index}] requires numeric "
                    "distance_from_left and height_from_floor"
                )
                continue
            if distance < 0 or height <= 0:
                problems.append(
                    f"measured_space.ceiling_points[{index}] requires non-negative "
                    "distance and positive height"
                )
                continue
            points.append(CeilingPoint(float(distance) * scale, float(height) * scale))
        self._check_full_width(points, raw_points, width_mm, problems)
        return tuple(points)

    def _check_full_width(
        self,
        points: list[CeilingPoint],
        raw_points: list[Any],
        width_mm: float,
        problems: list[str],
    ) -> None:
        if len(points) != len(raw_points):
            return
        distances = [point.distance_from_left_mm for point in points]
        if distances[0] != 0 or distances[-1] != width_mm:
            problems.append("ceiling points must start at 0 and end at measured_space.width")
        if any(left >= right for left, right in zip(distances, distances[1:])):
            problems.append("ceiling point distances must increase from left to right")
