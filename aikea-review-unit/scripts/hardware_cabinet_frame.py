"""Scope: Compose one saved hardware placement into cabinet coordinates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class HardwareCabinetFrame:
    """Keep one hardware origin and basis expressed in cabinet coordinates."""

    origin_mm: Vector3D
    x_axis: Vector3D
    y_axis: Vector3D
    z_axis: Vector3D

    def matches(self, other: "HardwareCabinetFrame", tolerance_mm: float) -> bool:
        values = zip(
            self.origin_mm + self.x_axis + self.y_axis + self.z_axis,
            other.origin_mm + other.x_axis + other.y_axis + other.z_axis,
        )
        return all(abs(left - right) <= tolerance_mm for left, right in values)

    def as_dict(self) -> dict[str, list[float]]:
        return {
            "origin_mm": list(self.origin_mm),
            "native_x_in_cabinet": list(self.x_axis),
            "native_y_in_cabinet": list(self.y_axis),
            "native_z_in_cabinet": list(self.z_axis),
        }


class HardwareCabinetFrameComposer:
    """Apply an optional owner frame to one saved local hardware frame."""

    _IDENTITY_ORIGIN: Vector3D = (0.0, 0.0, 0.0)
    _IDENTITY_AXES: tuple[Vector3D, Vector3D, Vector3D] = (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )

    def compose(
        self,
        placement: Any,
        owner_placement: Any | None = None,
    ) -> HardwareCabinetFrame:
        owner_origin, owner_axes = self._values(owner_placement)
        local_origin, local_axes = self._values(placement)
        return HardwareCabinetFrame(
            self._point(owner_origin, owner_axes, local_origin),
            self._direction(owner_axes, local_axes[0]),
            self._direction(owner_axes, local_axes[1]),
            self._direction(owner_axes, local_axes[2]),
        )

    def _values(
        self,
        placement: Any | None,
    ) -> tuple[Vector3D, tuple[Vector3D, Vector3D, Vector3D]]:
        if placement is None:
            return self._IDENTITY_ORIGIN, self._IDENTITY_AXES
        origin = placement.origin_in_parent
        basis = placement.axis_basis
        axes = tuple(
            (axis.x, axis.y, axis.z)
            for axis in (
                basis.local_x_in_parent,
                basis.local_y_in_parent,
                basis.local_z_in_parent,
            )
        )
        return (origin.x_mm, origin.y_mm, origin.z_mm), axes

    def _point(
        self,
        origin: Vector3D,
        axes: tuple[Vector3D, Vector3D, Vector3D],
        local: Vector3D,
    ) -> Vector3D:
        direction = self._direction(axes, local)
        return tuple(value + offset for value, offset in zip(origin, direction))

    def _direction(
        self,
        axes: tuple[Vector3D, Vector3D, Vector3D],
        local: Vector3D,
    ) -> Vector3D:
        return tuple(
            sum(local[index] * axes[index][component] for index in range(3))
            for component in range(3)
        )


__all__ = ["HardwareCabinetFrame", "HardwareCabinetFrameComposer", "Vector3D"]
