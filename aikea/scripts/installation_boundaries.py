"""Scope: Preserve which room edges physically constrain the furniture run."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fitted_dimensions import FittedDimensions


@dataclass(frozen=True, slots=True)
class InstallationBoundaries:
    """Name the measured room planes available to later movement checks."""

    left: bool
    right: bool
    top: bool


class InstallationBoundaryReader:
    """Read individual room boundaries without breaking older project files."""

    _SIDES = ("left", "right", "top")

    def read(
        self,
        data: dict[str, Any],
        fitted: FittedDimensions,
        problems: list[str],
    ) -> InstallationBoundaries:
        settings = data.get("design_settings")
        raw = settings.get("installation_boundaries") if isinstance(settings, dict) else None
        if raw is None:
            return InstallationBoundaries(fitted.width, fitted.width, fitted.height)
        values = self._read_values(raw, problems)
        self._check_fitted_dimensions(values, fitted, problems)
        return InstallationBoundaries(**values)

    def _read_values(
        self,
        raw: Any,
        problems: list[str],
    ) -> dict[str, bool]:
        if not isinstance(raw, dict):
            problems.append("design_settings.installation_boundaries must be a mapping")
            return dict.fromkeys(self._SIDES, False)
        values: dict[str, bool] = {}
        for side in self._SIDES:
            value = raw.get(side)
            if type(value) is not bool:
                problems.append(
                    f"design_settings.installation_boundaries.{side} "
                    "is required and must be true or false"
                )
                value = False
            values[side] = value
        return values

    def _check_fitted_dimensions(
        self,
        boundaries: dict[str, bool],
        fitted: FittedDimensions,
        problems: list[str],
    ) -> None:
        if fitted.width != (boundaries["left"] and boundaries["right"]):
            problems.append(
                "fitted width must match whether both left and right boundaries are fixed"
            )
        if fitted.height != boundaries["top"]:
            problems.append(
                "fitted height must match whether the top boundary is fixed"
            )


__all__ = ["InstallationBoundaries", "InstallationBoundaryReader"]
