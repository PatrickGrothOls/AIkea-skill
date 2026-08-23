"""Scope: Read one named set of three required space measurements."""

from __future__ import annotations

from typing import Any


class ThreePointMeasurementReader:
    """Read three positive measurements from their named physical locations."""

    def read(
        self,
        raw_measurements: Any,
        path: str,
        positions: tuple[str, str, str],
        scale: float,
        problems: list[str],
    ) -> tuple[float, ...]:
        if not isinstance(raw_measurements, dict):
            problems.append(f"{path} must contain {', '.join(positions)} measurements")
            return ()
        values: list[float] = []
        for position in positions:
            value = raw_measurements.get(position)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                problems.append(f"{path}.{position} is required and must be numeric")
                continue
            if value <= 0:
                problems.append(f"{path}.{position} must be greater than zero")
                continue
            values.append(float(value) * scale)
        return tuple(values)
