"""Scope: Calculate shared cabinet dimensions from checked overall inputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from ceiling_points import CeilingPoint
from overall_wardrobe_inputs import OverallWardrobeInputError, OverallWardrobeInputs


@dataclass(frozen=True)
class CabinetOverallSize:
    cabinet_number: int
    left_position_mm: float
    right_position_mm: float
    width_mm: float
    left_height_mm: float
    right_height_mm: float
    door_width_mm: float


@dataclass(frozen=True)
class OverallWardrobeResult:
    width_mm: float
    finished_depth_mm: float
    cabinet_depth_mm: float
    inside_depth_mm: float
    cabinets: tuple[CabinetOverallSize, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "width_mm": self.width_mm,
            "finished_depth_mm": self.finished_depth_mm,
            "cabinet_depth_mm": self.cabinet_depth_mm,
            "inside_depth_mm": self.inside_depth_mm,
            "cabinets": [asdict(cabinet) for cabinet in self.cabinets],
        }


class OverallWardrobeCalculator:
    """Distribute cabinet widths and sample the measured ceiling above each boundary."""

    def calculate(self, inputs: OverallWardrobeInputs) -> OverallWardrobeResult:
        problems = self._find_impossible_dimensions(inputs)
        if problems:
            raise OverallWardrobeInputError(problems)
        total_gaps = inputs.cabinet_gap_mm * (inputs.cabinet_count - 1)
        distributable_width = (
            inputs.width_mm - inputs.left_clearance_mm - inputs.right_clearance_mm - total_gaps
        )
        width_per_share = distributable_width / sum(inputs.cabinet_width_shares)
        cabinet_depth = inputs.depth_mm - inputs.door_thickness_mm
        inside_depth = cabinet_depth - inputs.back_panel_thickness_mm
        cabinets: list[CabinetOverallSize] = []
        left_position = inputs.left_clearance_mm
        for index, share in enumerate(inputs.cabinet_width_shares):
            width = width_per_share * share
            right_position = left_position + width
            left_height = self._cabinet_height_at(inputs, left_position)
            right_height = self._cabinet_height_at(inputs, right_position)
            cabinets.append(
                CabinetOverallSize(
                    cabinet_number=index + 1,
                    left_position_mm=left_position,
                    right_position_mm=right_position,
                    width_mm=width,
                    left_height_mm=left_height,
                    right_height_mm=right_height,
                    door_width_mm=width - inputs.door_gap_mm,
                )
            )
            left_position = right_position + inputs.cabinet_gap_mm
        return OverallWardrobeResult(
            width_mm=inputs.width_mm,
            finished_depth_mm=inputs.depth_mm,
            cabinet_depth_mm=cabinet_depth,
            inside_depth_mm=inside_depth,
            cabinets=tuple(cabinets),
        )

    def _find_impossible_dimensions(self, inputs: OverallWardrobeInputs) -> list[str]:
        problems: list[str] = []
        used_width = (
            inputs.left_clearance_mm
            + inputs.right_clearance_mm
            + inputs.cabinet_gap_mm * (inputs.cabinet_count - 1)
        )
        if used_width >= inputs.width_mm:
            problems.append("clearances and cabinet gaps leave no width for cabinets")
        if inputs.door_thickness_mm + inputs.back_panel_thickness_mm >= inputs.depth_mm:
            problems.append("door and back thicknesses leave no positive inside depth")
        available_width = inputs.width_mm - used_width
        narrowest_width = (
            available_width
            * min(inputs.cabinet_width_shares)
            / sum(inputs.cabinet_width_shares)
        )
        if inputs.door_gap_mm >= narrowest_width:
            problems.append("door gap must be smaller than every cabinet width")
        minimum_ceiling = min(point.height_from_floor_mm for point in inputs.ceiling_points)
        if inputs.base_height_mm + inputs.ceiling_clearance_mm >= minimum_ceiling:
            problems.append("base and ceiling clearance leave no positive cabinet height")
        return problems

    def _cabinet_height_at(self, inputs: OverallWardrobeInputs, position_mm: float) -> float:
        ceiling_height = self._ceiling_height_at(inputs.ceiling_points, position_mm)
        return ceiling_height - inputs.base_height_mm - inputs.ceiling_clearance_mm

    def _ceiling_height_at(
        self, points: tuple[CeilingPoint, ...], position_mm: float
    ) -> float:
        for left, right in zip(points, points[1:]):
            if left.distance_from_left_mm <= position_mm <= right.distance_from_left_mm:
                run = right.distance_from_left_mm - left.distance_from_left_mm
                fraction = (position_mm - left.distance_from_left_mm) / run
                rise = right.height_from_floor_mm - left.height_from_floor_mm
                return left.height_from_floor_mm + rise * fraction
        raise OverallWardrobeInputError(
            [f"no ceiling measurement covers position {position_mm} mm"]
        )
