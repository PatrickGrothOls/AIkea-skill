"""Scope: Read one or three horizontal measurements based on required fit."""

from __future__ import annotations

from typing import Any


class HorizontalMeasurementReader:
    """Read the required positive measurements for one horizontal dimension."""

    def read(
        self,
        raw_measurements: Any,
        path: str,
        is_fitted: bool,
        positions: tuple[str, str, str],
        scale: float,
        problems: list[str],
    ) -> tuple[float, ...]:
        if not isinstance(raw_measurements, dict):
            requirement = (
                ", ".join(positions) if is_fitted else "a single measurement"
            )
            problems.append(f"{path} must contain {requirement}")
            return ()
        if not is_fitted and "single" in raw_measurements:
            return self.read_single(raw_measurements, path, scale, problems)
        values = [
            self._read_positive_number(
                raw_measurements.get(position), f"{path}.{position}", scale, problems
            )
            for position in positions
        ]
        return tuple(value for value in values if value is not None)

    def read_single(
        self,
        raw_measurements: Any,
        path: str,
        scale: float,
        problems: list[str],
    ) -> tuple[float, ...]:
        if not isinstance(raw_measurements, dict):
            problems.append(f"{path} must contain a single measurement")
            return ()
        value = self._read_positive_number(
            raw_measurements.get("single"), f"{path}.single", scale, problems
        )
        return (value,) if value is not None else ()

    def _read_positive_number(
        self, value: Any, path: str, scale: float, problems: list[str]
    ) -> float | None:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            problems.append(f"{path} is required and must be numeric")
            return None
        if value <= 0:
            problems.append(f"{path} must be greater than zero")
            return None
        return float(value) * scale
