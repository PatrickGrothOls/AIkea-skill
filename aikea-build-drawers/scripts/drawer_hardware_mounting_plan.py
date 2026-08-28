"""Scope: Keep resolved purchased-hardware frames with their assembly owners."""

from __future__ import annotations

from dataclasses import dataclass

Vector3D = tuple[float, float, float]

SOURCE_CAD_MOUNTING_PLAN_SAVED = "source_cad_mounting_plan_saved"


@dataclass(frozen=True, slots=True)
class HardwarePlacement:
    """Place unchanged manufacturer CAD inside one immediate owner."""

    origin_mm: Vector3D
    local_x_in_owner: Vector3D
    local_y_in_owner: Vector3D
    local_z_in_owner: Vector3D


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
