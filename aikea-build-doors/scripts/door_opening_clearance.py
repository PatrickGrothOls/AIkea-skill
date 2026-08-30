"""Scope: Prove one hinged door clears measured room boundaries through 90 degrees."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from door_hinge_side import DoorHingeSide
from door_opening_sweep import DoorOpeningSweep
from riex_nc70_hinge_pivot import RiexNc70HingePivot
from riex_nc70_hinge_profile import RiexNc70HingeProfile


@dataclass(frozen=True, slots=True)
class DoorOpeningClearanceResult:
    """Record the checked side, boundary clearances, and supported conclusion."""

    hinge_side: DoorHingeSide
    required_angle_degrees: float
    boundary_clearances_mm: tuple[tuple[str, float], ...]
    issues: tuple[str, ...]

    @property
    def passes(self) -> bool:
        return not self.issues


class DoorOpeningClearanceChecker:
    """Apply explicit room-boundary policy to one generated door sweep."""

    def __init__(self) -> None:
        self.hinge_pivot = RiexNc70HingePivot()

    def check(
        self,
        inputs: Any,
        assembly: Any,
        hinge_side: DoorHingeSide,
        profile: RiexNc70HingeProfile,
    ) -> DoorOpeningClearanceResult:
        door = assembly.part("door_panel")
        pivot = self.hinge_pivot.resolve(assembly, profile, hinge_side)
        sweep = DoorOpeningSweep(assembly, door, pivot, hinge_side)
        boundaries = inputs.settings.installation_boundaries
        left_mm, right_mm = sweep.horizontal_extent_mm
        clearances: list[tuple[str, float]] = []
        issues: list[str] = []
        if boundaries.left:
            self._record("left", left_mm, clearances, issues)
        if boundaries.right:
            self._record(
                "right",
                inputs.space.minimum_width_mm - right_mm,
                clearances,
                issues,
            )
        if boundaries.top:
            ceiling_clearance = self._ceiling_clearance(inputs, sweep)
            if ceiling_clearance is None:
                issues.append(
                    "measured top boundary does not cover the complete 90 degree sweep"
                )
            else:
                self._record("top", ceiling_clearance, clearances, issues)
        return DoorOpeningClearanceResult(
            hinge_side,
            sweep.REQUIRED_ANGLE_DEGREES,
            tuple(clearances),
            tuple(issues),
        )

    def _ceiling_clearance(
        self,
        inputs: Any,
        sweep: DoorOpeningSweep,
    ) -> float | None:
        measurements = inputs.space.top_boundary.measurements
        covered = (
            measurements[0].distance_from_left_mm,
            measurements[-1].distance_from_left_mm,
        )
        minimum = float("inf")
        for sample in sweep.top_samples():
            if not covered[0] <= sample.x_mm <= covered[1]:
                return None
            ceiling_mm = inputs.space.top_boundary.height_at(sample.x_mm)
            minimum = min(minimum, ceiling_mm - sample.height_mm)
        ceiling_slope = self._maximum_ceiling_slope(inputs)
        error_mm = (
            ceiling_slope
            * sweep.maximum_radius_mm
            * sweep.angular_half_step_radians
            + (ceiling_slope + sweep.top.maximum_slope) * sweep.top_half_step_mm
        )
        return minimum - error_mm

    def _maximum_ceiling_slope(self, inputs: Any) -> float:
        points = inputs.space.top_boundary.measurements
        return max(
            (
                abs(right.height_from_floor_mm - left.height_from_floor_mm)
                / (right.distance_from_left_mm - left.distance_from_left_mm)
                for left, right in zip(points, points[1:])
            ),
            default=0.0,
        )

    def _record(
        self,
        boundary: str,
        clearance_mm: float,
        clearances: list[tuple[str, float]],
        issues: list[str],
    ) -> None:
        clearances.append((boundary, round(clearance_mm, 3)))
        if clearance_mm < 0.0:
            issues.append(f"{boundary} room boundary is crossed before 90 degrees")


__all__ = ["DoorOpeningClearanceChecker", "DoorOpeningClearanceResult"]
