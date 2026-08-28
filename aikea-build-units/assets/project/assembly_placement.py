"""Scope: Define explicit local-to-parent coordinates for nested assembly items."""

from __future__ import annotations

from dataclasses import dataclass


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
