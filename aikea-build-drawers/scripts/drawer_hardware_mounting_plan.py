"""Scope: Keep resolved purchased-hardware frames with their assembly owners."""

from __future__ import annotations

from dataclasses import dataclass

from hardware_placement import HardwarePlacement, Vector3D

SOURCE_CAD_MOUNTING_PLAN_SAVED = "source_cad_mounting_plan_saved"


@dataclass(frozen=True, slots=True)
class DrawerHardwareMountingPlan:
    """Own the fixed runner frames and moving locking-device frames."""

    runner_left_in_cabinet: HardwarePlacement
    runner_right_in_cabinet: HardwarePlacement
    locking_device_left_in_drawer: HardwarePlacement
    locking_device_right_in_drawer: HardwarePlacement
    geometry_state: str = SOURCE_CAD_MOUNTING_PLAN_SAVED


__all__ = [
    "DrawerHardwareMountingPlan",
    "HardwarePlacement",
    "SOURCE_CAD_MOUNTING_PLAN_SAVED",
    "Vector3D",
]
