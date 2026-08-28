"""Scope: Define explicit local-to-parent coordinates for nested assembly items."""

from __future__ import annotations

from dataclasses import dataclass


class AssemblyPlacementError(ValueError):
    """Report a saved frame that cannot represent a rigid assembly placement."""


@dataclass(frozen=True)
class Point3D:
    """Locate one origin in millimetres."""

    x_mm: float
    y_mm: float
    z_mm: float


@dataclass(frozen=True)
class AxisDirection:
    """Express one local unit axis in its parent coordinate frame."""

    x: float
    y: float
    z: float


@dataclass(frozen=True)
class AxisBasis:
    """Name all three local axes as directions in the parent frame."""

    local_x_in_parent: AxisDirection
    local_y_in_parent: AxisDirection
    local_z_in_parent: AxisDirection

    def __post_init__(self) -> None:
        vectors = tuple(
            (direction.x, direction.y, direction.z)
            for direction in (
                self.local_x_in_parent,
                self.local_y_in_parent,
                self.local_z_in_parent,
            )
        )
        lengths_are_one = all(
            abs(sum(component * component for component in vector) ** 0.5 - 1.0)
            <= 1e-9
            for vector in vectors
        )
        axes_are_orthogonal = all(
            abs(sum(a * b for a, b in zip(left, right))) <= 1e-9
            for left, right in (
                (vectors[0], vectors[1]),
                (vectors[0], vectors[2]),
                (vectors[1], vectors[2]),
            )
        )
        x_axis, y_axis, z_axis = vectors
        derived_z = (
            x_axis[1] * y_axis[2] - x_axis[2] * y_axis[1],
            x_axis[2] * y_axis[0] - x_axis[0] * y_axis[2],
            x_axis[0] * y_axis[1] - x_axis[1] * y_axis[0],
        )
        is_right_handed = all(
            abs(actual - expected) <= 1e-9
            for actual, expected in zip(derived_z, z_axis)
        )
        if not (lengths_are_one and axes_are_orthogonal and is_right_handed):
            raise AssemblyPlacementError(
                "local-to-parent axes must form an orthonormal right-handed basis"
            )


@dataclass(frozen=True)
class LocalToParentPlacement:
    """Place one local coordinate frame inside its immediate parent."""

    origin_in_parent: Point3D
    axis_basis: AxisBasis


IDENTITY_AXIS_BASIS = AxisBasis(
    local_x_in_parent=AxisDirection(1.0, 0.0, 0.0),
    local_y_in_parent=AxisDirection(0.0, 1.0, 0.0),
    local_z_in_parent=AxisDirection(0.0, 0.0, 1.0),
)
IDENTITY_LOCAL_TO_PARENT = LocalToParentPlacement(
    origin_in_parent=Point3D(0.0, 0.0, 0.0),
    axis_basis=IDENTITY_AXIS_BASIS,
)
