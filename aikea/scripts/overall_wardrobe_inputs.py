"""Scope: Compose checked space measurements and overall wardrobe settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from design_decisions import DesignDecision, DesignDecisionReader
from material_decision_gate import MaterialDecisionGate
from overall_design_settings import OverallDesignSettingReader, OverallDesignSettings
from overall_space_measurements import OverallSpaceMeasurementReader, OverallSpaceMeasurements


class OverallWardrobeInputError(ValueError):
    """Report every problem that prevents overall calculations."""

    def __init__(self, problems: list[str]) -> None:
        super().__init__("\n".join(problems))
        self.problems = tuple(problems)


@dataclass(frozen=True)
class OverallWardrobeInputs:
    space: OverallSpaceMeasurements
    settings: OverallDesignSettings
    design_decisions: tuple[DesignDecision, ...]


class OverallWardrobeInputReader:
    """Turn user-editable YAML data into checked millimetre inputs."""

    def read(self, data: dict[str, Any]) -> OverallWardrobeInputs:
        problems: list[str] = []
        self._check_schema_version(data, problems)
        scale = self._read_unit_scale(data, problems)
        design_decisions = DesignDecisionReader().read(data, problems)
        problems.extend(MaterialDecisionGate().problems(design_decisions))
        settings = OverallDesignSettingReader().read(data, scale, problems)
        allowances = settings.fitted_dimensions.resolve_fitting_allowances(
            settings.fit_allowance_mm
        )
        space = OverallSpaceMeasurementReader().read(
            data,
            scale,
            settings.fitted_dimensions,
            allowances.width_mm,
            problems,
        )
        if problems:
            raise OverallWardrobeInputError(problems)
        return OverallWardrobeInputs(
            space=space,
            settings=settings,
            design_decisions=design_decisions,
        )

    def _check_schema_version(self, data: dict[str, Any], problems: list[str]) -> None:
        if (
            type(data.get("schema_version")) is not int
            or data["schema_version"] not in (8, 9)
        ):
            problems.append("schema_version must be 8 or 9")

    def _read_unit_scale(self, data: dict[str, Any], problems: list[str]) -> float:
        unit = data.get("units")
        scales = {"mm": 1.0, "cm": 10.0, "in": 25.4}
        if unit not in scales:
            problems.append("units must be 'mm', 'cm', or 'in'")
            return 1.0
        return scales[unit]
