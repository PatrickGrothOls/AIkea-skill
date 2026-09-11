"""Scope: Transform points between one rigid hardware frame and its immediate owner."""

from __future__ import annotations

from dataclasses import dataclass

Vector3D = tuple[float, float, float]


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


__all__ = ["HardwarePlacement", "Vector3D"]
