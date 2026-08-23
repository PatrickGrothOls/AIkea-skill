"""Scope: Read the repeated width, depth, and height measurements of one space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from enclosed_dimensions import EnclosedDimensions
from height_measurements import HeightMeasurement, HeightMeasurementReader
from horizontal_measurements import HorizontalMeasurementReader


@dataclass(frozen=True)
class OverallSpaceMeasurements:
    width_measurements_mm: tuple[float, ...]
    depth_measurements_mm: tuple[float, ...]
    height_measurements: tuple[HeightMeasurement, ...]

    @property
    def minimum_width_mm(self) -> float:
        return min(self.width_measurements_mm)

    @property
    def minimum_depth_mm(self) -> float:
        return min(self.depth_measurements_mm)


class OverallSpaceMeasurementReader:
    """Turn the client's site readings into one checked measured-space value."""

    def read(
        self,
        data: dict[str, Any],
        scale: float,
        enclosed_dimensions: EnclosedDimensions,
        width_fitting_allowance_mm: float,
        problems: list[str],
    ) -> OverallSpaceMeasurements:
        measured_space = data.get("measured_space")
        if not isinstance(measured_space, dict):
            measured_space = {}
        reader = HorizontalMeasurementReader()
        widths = reader.read(
            measured_space.get("width_measurements"),
            "measured_space.width_measurements",
            enclosed_dimensions.width,
            ("bottom", "middle", "top"),
            scale,
            problems,
        )
        depths = reader.read(
            measured_space.get("depth_measurements"),
            "measured_space.depth_measurements",
            enclosed_dimensions.depth,
            ("left", "middle", "right"),
            scale,
            problems,
        )
        usable_width = max(
            min(widths, default=0.0) - width_fitting_allowance_mm,
            0.0,
        )
        heights = HeightMeasurementReader().read(
            measured_space.get("height_measurements"),
            usable_width,
            enclosed_dimensions.height,
            scale,
            problems,
        )
        return OverallSpaceMeasurements(widths, depths, heights)
