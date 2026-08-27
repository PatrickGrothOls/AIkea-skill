"""Scope: Read the shared door-bottom and plinth-front design choices."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class DoorBottom(str, Enum):
    """Name the lower line reached by a closed door."""

    FLOOR = "floor"
    PLINTH = "plinth"


class PlinthFront(str, Enum):
    """Name whether the visible plinth front aligns with the cabinet front."""

    FLUSH = "flush"
    RECESSED = "recessed"


@dataclass(frozen=True)
class DoorAndPlinthSettings:
    door_bottom: DoorBottom
    plinth_front: PlinthFront
    plinth_recess_mm: float


class DoorAndPlinthSettingReader:
    """Turn the two independent lower-front choices into checked settings."""

    def read(
        self,
        data: dict[str, Any],
        scale: float,
        problems: list[str],
    ) -> DoorAndPlinthSettings:
        if data.get("schema_version") == 8:
            return DoorAndPlinthSettings(
                DoorBottom.FLOOR,
                PlinthFront.FLUSH,
                0.0,
            )
        door_bottom = self._choice(
            data,
            "design_settings.doors.bottom",
            DoorBottom,
            problems,
        )
        plinth_front = self._choice(
            data,
            "design_settings.base.front",
            PlinthFront,
            problems,
        )
        recess_mm = self._recess(data, scale, problems)
        if plinth_front is PlinthFront.FLUSH and recess_mm != 0.0:
            problems.append("design_settings.base.recess must be zero when the front is flush")
        if plinth_front is PlinthFront.RECESSED and recess_mm <= 0.0:
            problems.append(
                "design_settings.base.recess must be greater than zero when the front is recessed"
            )
        return DoorAndPlinthSettings(
            door_bottom or DoorBottom.FLOOR,
            plinth_front or PlinthFront.FLUSH,
            recess_mm,
        )

    def _choice(self, data, path, choices, problems):
        value = self._read_path(data, path)
        try:
            return choices(value)
        except ValueError:
            allowed = " or ".join(repr(choice.value) for choice in choices)
            problems.append(f"{path} must be {allowed}")
            return None

    def _recess(
        self,
        data: dict[str, Any],
        scale: float,
        problems: list[str],
    ) -> float:
        path = "design_settings.base.recess"
        value = self._read_path(data, path)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            problems.append(f"{path} is required and must be numeric")
            return 0.0
        if value < 0:
            problems.append(f"{path} must be zero or greater")
        return float(value) * scale

    def _read_path(self, data: dict[str, Any], path: str) -> Any:
        value: Any = data
        for key in path.split("."):
            if not isinstance(value, dict):
                return None
            value = value.get(key)
        return value


__all__ = [
    "DoorAndPlinthSettingReader",
    "DoorAndPlinthSettings",
    "DoorBottom",
    "PlinthFront",
]
