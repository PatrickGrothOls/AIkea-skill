"""Scope: Read and validate measured floor-to-ceiling heights from left to right."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class HeightMeasurement:
    distance_from_left_mm: float
    height_from_floor_mm: float


class HeightMeasurementReader:
    """Turn editable height readings into checked millimetre measurements."""

    def read(
        self,
        raw_measurements: Any,
        required_width_mm: float,
        is_fitted: bool,
        scale: float,
        problems: list[str],
    ) -> tuple[HeightMeasurement, ...]:
        path = "measured_space.height_measurements"
        minimum_count = 3 if is_fitted else 1
        if (
            not isinstance(raw_measurements, list)
            or len(raw_measurements) < minimum_count
        ):
            count = "at least three" if is_fitted else "at least one"
            suffix = "s" if is_fitted else ""
            problems.append(f"{path} must contain {count} measurement{suffix}")
            return ()
        measurements: list[HeightMeasurement] = []
        for index, raw in enumerate(raw_measurements):
            measurement = self._read_measurement(raw, path, index, scale, problems)
            if measurement:
                measurements.append(measurement)
        self._check_coverage(measurements, raw_measurements, required_width_mm, problems)
        return tuple(measurements)

    def _read_measurement(
        self,
        raw: Any,
        path: str,
        index: int,
        scale: float,
        problems: list[str],
    ) -> HeightMeasurement | None:
        if not isinstance(raw, dict):
            problems.append(f"{path}[{index}] must be an object")
            return None
        distance = raw.get("distance_from_left")
        height = raw.get("height_from_floor")
        if any(
            isinstance(value, bool) or not isinstance(value, (int, float))
            for value in (distance, height)
        ):
            problems.append(
                f"{path}[{index}] requires numeric distance_from_left and height_from_floor"
            )
            return None
        if distance < 0 or height <= 0:
            problems.append(
                f"{path}[{index}] requires non-negative distance and positive height"
            )
            return None
        return HeightMeasurement(float(distance) * scale, float(height) * scale)

    def _check_coverage(
        self,
        measurements: list[HeightMeasurement],
        raw_measurements: list[Any],
        required_width_mm: float,
        problems: list[str],
    ) -> None:
        if len(measurements) != len(raw_measurements):
            return
        if len(measurements) == 1:
            return
        distances = [measurement.distance_from_left_mm for measurement in measurements]
        if distances[0] != 0 or distances[-1] < required_width_mm:
            problems.append("height measurements must start at 0 and cover the usable width")
        if any(left >= right for left, right in zip(distances, distances[1:])):
            problems.append("height measurement distances must increase from left to right")
