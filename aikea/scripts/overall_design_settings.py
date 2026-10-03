"""Scope: Read and validate shared wardrobe choices that drive overall geometry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from door_and_plinth_settings import (
    DoorAndPlinthSettingReader,
    DoorBottom,
    PlinthFront,
)
from fitted_dimensions import FittedDimensionReader, FittedDimensions
from installation_boundaries import InstallationBoundaries, InstallationBoundaryReader


@dataclass(frozen=True)
class OverallDesignSettings:
    fit_allowance_mm: float
    fitted_dimensions: FittedDimensions
    installation_boundaries: InstallationBoundaries
    cabinet_count: int
    cabinet_width_shares: tuple[float, ...]
    left_clearance_mm: float
    right_clearance_mm: float
    cabinet_gap_mm: float
    ceiling_clearance_mm: float
    base_height_mm: float
    door_gap_mm: float
    door_bottom: DoorBottom
    plinth_front: PlinthFront
    plinth_recess_mm: float
    cabinet_panel_thickness_mm: float
    door_thickness_mm: float
    back_panel_thickness_mm: float


class OverallDesignSettingReader:
    """Turn editable shared choices into checked millimetre settings."""

    _NUMBER_PATHS = (
        ("design_settings.fit_allowance", True),
        ("design_settings.cabinet_run.left_clearance", True),
        ("design_settings.cabinet_run.right_clearance", True),
        ("design_settings.cabinet_run.cabinet_gap", True),
        ("design_settings.cabinet_run.ceiling_clearance", True),
        ("design_settings.base.height", False),
        ("design_settings.doors.gap", True),
        ("design_settings.materials.cabinet_panel_thickness", False),
        ("design_settings.materials.door_thickness", False),
        ("design_settings.materials.back_panel_thickness", False),
    )

    def read(
        self, data: dict[str, Any], scale: float, problems: list[str]
    ) -> OverallDesignSettings:
        numbers = {
            path: self._read_number(data, path, allow_zero, scale, problems)
            for path, allow_zero in self._NUMBER_PATHS
        }
        cabinet_count = self._read_cabinet_count(data, problems)
        shares = self._read_width_shares(data, cabinet_count, problems)
        lower_front = DoorAndPlinthSettingReader().read(data, scale, problems)
        fitted_dimensions = FittedDimensionReader().read(data, problems)
        return OverallDesignSettings(
            fit_allowance_mm=numbers["design_settings.fit_allowance"],
            fitted_dimensions=fitted_dimensions,
            installation_boundaries=InstallationBoundaryReader().read(
                data,
                fitted_dimensions,
                problems,
            ),
            cabinet_count=cabinet_count,
            cabinet_width_shares=shares,
            left_clearance_mm=numbers["design_settings.cabinet_run.left_clearance"],
            right_clearance_mm=numbers["design_settings.cabinet_run.right_clearance"],
            cabinet_gap_mm=numbers["design_settings.cabinet_run.cabinet_gap"],
            ceiling_clearance_mm=numbers["design_settings.cabinet_run.ceiling_clearance"],
            base_height_mm=numbers["design_settings.base.height"],
            door_gap_mm=numbers["design_settings.doors.gap"],
            door_bottom=lower_front.door_bottom,
            plinth_front=lower_front.plinth_front,
            plinth_recess_mm=lower_front.plinth_recess_mm,
            cabinet_panel_thickness_mm=numbers[
                "design_settings.materials.cabinet_panel_thickness"
            ],
            door_thickness_mm=numbers["design_settings.materials.door_thickness"],
            back_panel_thickness_mm=numbers[
                "design_settings.materials.back_panel_thickness"
            ],
        )

    def _read_number(
        self,
        data: dict[str, Any],
        path: str,
        allow_zero: bool,
        scale: float,
        problems: list[str],
    ) -> float:
        value = self._read_path(data, path)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            problems.append(f"{path} is required and must be numeric")
            return 0.0
        if value < 0 or (not allow_zero and value == 0):
            rule = "zero or greater" if allow_zero else "greater than zero"
            problems.append(f"{path} must be {rule}")
        return float(value) * scale

    def _read_cabinet_count(self, data: dict[str, Any], problems: list[str]) -> int:
        path = "design_settings.cabinet_run.cabinet_count"
        value = self._read_path(data, path)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            problems.append(f"{path} is required and must be a positive whole number")
            return 0
        return value

    def _read_width_shares(
        self, data: dict[str, Any], cabinet_count: int, problems: list[str]
    ) -> tuple[float, ...]:
        path = "design_settings.cabinet_run.cabinet_width_shares"
        values = self._read_path(data, path)
        if not isinstance(values, list):
            problems.append(f"{path} is required and must be a list")
            return ()
        if cabinet_count and len(values) != cabinet_count:
            problems.append(f"{path} must contain one share for each cabinet")
        if any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0
            for value in values
        ):
            problems.append(f"{path} values must all be greater than zero")
            return ()
        return tuple(float(value) for value in values)

    def _read_path(self, data: dict[str, Any], path: str) -> Any:
        value: Any = data
        for key in path.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(key)
        return value
