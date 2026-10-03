"""Scope: Locate each canonical drawer sheet inside its drawer-local frame."""

from __future__ import annotations

from dataclasses import dataclass

from drawer_box_spec import DrawerBoxSpec

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class DrawerPoint3D:
    """Express a drawer-local origin in millimetres."""

    x_mm: float
    y_mm: float
    z_mm: float


@dataclass(frozen=True, slots=True)
class DrawerAxisDirection:
    """Express one drawer-local unit axis in its parent frame."""

    x: float
    y: float
    z: float


@dataclass(frozen=True, slots=True)
class DrawerAxisBasis:
    """Use the same named axis contract as generated assembly placements."""

    local_x_in_parent: DrawerAxisDirection
    local_y_in_parent: DrawerAxisDirection
    local_z_in_parent: DrawerAxisDirection


@dataclass(frozen=True, slots=True)
class DrawerPartPlacement:
    """Expose one manufacturing-frame transform in drawer-local coordinates."""

    origin_in_parent: DrawerPoint3D
    axis_basis: DrawerAxisBasis


class DrawerPartLocator:
    """Calculate explicit placements for the five unmachined drawer sheets."""

    def placement(self, part_id: str, drawer: DrawerBoxSpec) -> DrawerPartPlacement:
        side_thickness_mm = drawer.sizing.side_thickness_mm
        front_back_thickness_mm = drawer.sizing.front_back_thickness_mm
        inside_right_mm = side_thickness_mm + drawer.clear_inside_width_mm
        inside_back_mm = drawer.outside_depth_mm - front_back_thickness_mm
        placements = {
            "left_side": self._placement(
                (side_thickness_mm, inside_back_mm, 0.0),
                (0.0, -1.0, 0.0),
                (-1.0, 0.0, 0.0),
            ),
            "right_side": self._placement(
                (inside_right_mm, front_back_thickness_mm, 0.0),
                (0.0, 1.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            "front": self._placement(
                (0.0, front_back_thickness_mm, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
            ),
            "back": self._placement(
                (drawer.outside_width_mm, inside_back_mm, 0.0),
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
            ),
            "bottom": self._placement(
                (
                    side_thickness_mm,
                    front_back_thickness_mm,
                    drawer.sizing.bottom_underside_recess_mm,
                ),
                (1.0, 0.0, 0.0),
                (0.0, 0.0, 1.0),
            ),
        }
        try:
            return placements[part_id]
        except KeyError as error:
            raise ValueError(f"no drawer placement exists for {part_id}") from error

    def _placement(
        self,
        origin: Vector3D,
        local_x: Vector3D,
        local_z: Vector3D,
    ) -> DrawerPartPlacement:
        local_y = (
            (local_z[1] * local_x[2]) - (local_z[2] * local_x[1]),
            (local_z[2] * local_x[0]) - (local_z[0] * local_x[2]),
            (local_z[0] * local_x[1]) - (local_z[1] * local_x[0]),
        )
        return DrawerPartPlacement(
            DrawerPoint3D(*origin),
            DrawerAxisBasis(
                DrawerAxisDirection(*local_x),
                DrawerAxisDirection(*local_y),
                DrawerAxisDirection(*local_z),
            ),
        )


__all__ = [
    "DrawerAxisBasis",
    "DrawerAxisDirection",
    "DrawerPartLocator",
    "DrawerPartPlacement",
    "DrawerPoint3D",
    "Vector3D",
]
