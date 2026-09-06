"""Scope: Carry exact KA 4532 and 13952 placements with their owners."""

from __future__ import annotations

from dataclasses import dataclass
from drawer_hardware_mounting_plan import HardwarePlacement

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class HettichKa4532SpacerMountingPlan:
    """Keep cabinet-owned and drawer-owned source-CAD frames together."""

    cabinet_front_mm: float
    drawer_front_mm: float
    drawer_origin_mm: Vector3D
    drawer_outside_width_mm: float
    spacer_left_in_cabinet: HardwarePlacement
    spacer_right_in_cabinet: HardwarePlacement
    fixed_runner_left_in_cabinet: HardwarePlacement
    fixed_runner_right_in_cabinet: HardwarePlacement
    moving_runner_left_in_drawer: HardwarePlacement
    moving_runner_right_in_drawer: HardwarePlacement


__all__ = ["HettichKa4532SpacerMountingPlan", "Vector3D"]
