"""Scope: Read the repeated width, depth, and height measurements of one space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fitted_dimensions import FittedDimensions
from horizontal_measurements import HorizontalMeasurementReader
from top_boundary import TopBoundary, TopBoundaryReader


@dataclass(frozen=True)
class OverallSpaceMeasurements:
    width_measurements_mm: tuple[float, ...]
    depth_measurements_mm: tuple[float, ...]
    top_boundary: TopBoundary

    @property
    def minimum_width_mm(self) -> float:
        return min(self.width_measurements_mm)

    @property
    def minimum_depth_mm(self) -> float:
        return min(self.depth_measurements_mm)

    @property
    def minimum_height_mm(self) -> float:
        return self.top_boundary.minimum_height_mm


class OverallSpaceMeasurementReader:
    """Turn the client's site readings into one checked measured-space value."""

    def read(
        self,
        data: dict[str, Any],
        scale: float,
        fitted_dimensions: FittedDimensions,
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
            fitted_dimensions.width,
            ("bottom", "middle", "top"),
            scale,
            problems,
        )
        if fitted_dimensions.depth:
            depths = reader.read(
                measured_space.get("depth_measurements"),
                "measured_space.depth_measurements",
                True,
                ("left", "middle", "right"),
                scale,
                problems,
            )
        else:
            depths = reader.read_single(
                measured_space.get("depth_measurements"),
                "measured_space.depth_measurements",
                scale,
                problems,
            )
        usable_width = max(
            min(widths, default=0.0) - width_fitting_allowance_mm,
            0.0,
        )
        top_boundary = TopBoundaryReader().read(
            measured_space,
            usable_width,
            fitted_dimensions.height,
            scale,
            problems,
        )
        return OverallSpaceMeasurements(widths, depths, top_boundary)
