"""Scope: Read fitted wardrobe dimensions and resolve their fitting allowances."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FittingAllowances:
    width_mm: float
    depth_mm: float
    height_mm: float


@dataclass(frozen=True)
class FittedDimensions:
    width: bool
    depth: bool
    height: bool

    def resolve_fitting_allowances(self, allowance_mm: float) -> FittingAllowances:
        return FittingAllowances(
            width_mm=allowance_mm if self.width else 0.0,
            depth_mm=allowance_mm if self.depth else 0.0,
            height_mm=allowance_mm if self.height else 0.0,
        )


class FittedDimensionReader:
    """Read which wardrobe dimensions must fit between fixed boundaries."""

    def read(self, data: dict[str, Any], problems: list[str]) -> FittedDimensions:
        settings = data.get("design_settings")
        raw = settings.get("fitted_dimensions") if isinstance(settings, dict) else {}
        values: dict[str, bool] = {}
        for dimension in ("width", "depth", "height"):
            value = raw.get(dimension) if isinstance(raw, dict) else None
            if type(value) is not bool:
                problems.append(
                    f"design_settings.fitted_dimensions.{dimension} "
                    "is required and must be true or false"
                )
                value = False
            values[dimension] = value
        return FittedDimensions(**values)
