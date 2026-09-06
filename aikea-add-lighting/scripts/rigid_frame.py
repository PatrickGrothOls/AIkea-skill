"""Scope: Convert a CadQuery location into inspectable origin and axis values."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


Vector3 = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class RigidFrame:
    """Expose one right-handed location without hiding its axis directions."""

    origin_mm: Vector3
    local_x_in_parent: Vector3
    local_y_in_parent: Vector3
    local_z_in_parent: Vector3

    @classmethod
    def from_location(cls, location: cq.Location) -> "RigidFrame":
        matrix = cq.Matrix(location.wrapped.Transformation())
        origin = cq.Vector(0.0, 0.0, 0.0).transform(matrix)
        axes = tuple(
            cq.Vector(*point).transform(matrix) - origin
            for point in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
        )
        return cls(
            origin.toTuple(),
            axes[0].toTuple(),
            axes[1].toTuple(),
            axes[2].toTuple(),
        )

    def as_record(self) -> dict[str, list[float]]:
        return {
            "origin_mm": list(self.origin_mm),
            "local_x_in_parent": list(self.local_x_in_parent),
            "local_y_in_parent": list(self.local_y_in_parent),
            "local_z_in_parent": list(self.local_z_in_parent),
        }

    def as_project_placement(self):
        from assemblies.specification import (
            AxisBasis,
            AxisDirection,
            LocalToParentPlacement,
            Point3D,
        )

        return LocalToParentPlacement(
            Point3D(*self.origin_mm),
            AxisBasis(
                AxisDirection(*self.local_x_in_parent),
                AxisDirection(*self.local_y_in_parent),
                AxisDirection(*self.local_z_in_parent),
            ),
        )


__all__ = ["RigidFrame", "Vector3"]
