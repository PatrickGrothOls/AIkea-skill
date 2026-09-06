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

    def to_owner(self, local_point: Vector3D) -> Vector3D:
        """Map one hardware-local point into its immediate owner."""
        return tuple(
            self.origin_mm[coordinate]
            + sum(
                local_point[axis] * self.axes[axis][coordinate]
                for axis in range(3)
            )
            for coordinate in range(3)
        )

    def to_local(self, owner_point: Vector3D) -> Vector3D:
        """Map one owner point back through this orthonormal frame."""
        delta = tuple(
            owner_point[index] - self.origin_mm[index] for index in range(3)
        )
        return tuple(
            sum(delta[index] * axis[index] for index in range(3))
            for axis in self.axes
        )

    @property
    def axes(self) -> tuple[Vector3D, Vector3D, Vector3D]:
        """Return the local basis in owner coordinates."""
        return (
            self.local_x_in_owner,
            self.local_y_in_owner,
            self.local_z_in_owner,
        )


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
