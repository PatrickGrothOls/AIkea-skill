"""Scope: Read and validate the editable overall wardrobe input file."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ceiling_points import CeilingPoint, CeilingPointReader


class OverallWardrobeInputError(ValueError):
    """Report every problem that prevents overall calculations."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("\n".join(problems))
        self.problems = tuple(problems)


@dataclass(frozen=True)
class OverallWardrobeInputs:
    width_mm: float
    depth_mm: float
    ceiling_points: tuple[CeilingPoint, ...]
    cabinet_count: int
    cabinet_width_shares: tuple[float, ...]
    left_clearance_mm: float
    right_clearance_mm: float
    cabinet_gap_mm: float
    ceiling_clearance_mm: float
    base_height_mm: float
    door_gap_mm: float
    cabinet_panel_thickness_mm: float
    door_thickness_mm: float
    back_panel_thickness_mm: float


class OverallWardrobeInputReader:
    """Turn user-editable YAML data into checked millimetre inputs."""

    _NUMBER_PATHS = (
        ("measured_space.width", False),
        ("measured_space.depth", False),
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

    def read(self, data: dict[str, Any]) -> OverallWardrobeInputs:
        problems: list[str] = []
        self._check_schema_version(data, problems)
        scale = self._read_unit_scale(data, problems)
        numbers = {
            path: self._read_number(data, path, allow_zero, scale, problems)
            for path, allow_zero in self._NUMBER_PATHS
        }
        cabinet_count = self._read_cabinet_count(data, problems)
        shares = self._read_width_shares(data, cabinet_count, problems)
        points = CeilingPointReader().read(
            self._read_path(data, "measured_space.ceiling_points"),
            numbers["measured_space.width"],
            scale,
            problems,
        )
        if problems:
            raise OverallWardrobeInputError(problems)
        return OverallWardrobeInputs(
            width_mm=numbers["measured_space.width"],
            depth_mm=numbers["measured_space.depth"],
            ceiling_points=points,
            cabinet_count=cabinet_count,
            cabinet_width_shares=shares,
            left_clearance_mm=numbers["design_settings.cabinet_run.left_clearance"],
            right_clearance_mm=numbers["design_settings.cabinet_run.right_clearance"],
            cabinet_gap_mm=numbers["design_settings.cabinet_run.cabinet_gap"],
            ceiling_clearance_mm=numbers["design_settings.cabinet_run.ceiling_clearance"],
            base_height_mm=numbers["design_settings.base.height"],
            door_gap_mm=numbers["design_settings.doors.gap"],
            cabinet_panel_thickness_mm=numbers["design_settings.materials.cabinet_panel_thickness"],
            door_thickness_mm=numbers["design_settings.materials.door_thickness"],
            back_panel_thickness_mm=numbers["design_settings.materials.back_panel_thickness"],
        )

    def _check_schema_version(self, data: dict[str, Any], problems: list[str]) -> None:
        if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
            problems.append("schema_version must be 1")

    def _read_unit_scale(self, data: dict[str, Any], problems: list[str]) -> float:
        unit = data.get("units")
        scales = {"mm": 1.0, "cm": 10.0}
        if unit not in scales:
            problems.append("units must be either 'mm' or 'cm'")
            return 1.0
        return scales[unit]

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
