"""Scope: Locate each canonical drawer sheet inside its drawer-local frame."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq

from drawer_box_spec import DrawerBoxSpec

Vector3D = tuple[float, float, float]


@dataclass(frozen=True, slots=True)
class DrawerPartPlacement:
    """Expose one manufacturing-frame transform in drawer-local coordinates."""

    origin_mm: Vector3D
    local_x_direction: Vector3D
    thickness_direction: Vector3D

    def location(self) -> cq.Location:
        return cq.Location(
            cq.Plane(
                origin=self.origin_mm,
                xDir=self.local_x_direction,
                normal=self.thickness_direction,
            )
        )


class DrawerPartLocator:
    """Calculate explicit placements for the five unmachined drawer sheets."""

    def placement(self, part_id: str, drawer: DrawerBoxSpec) -> DrawerPartPlacement:
        side_thickness_mm = drawer.sizing.side_thickness_mm
        front_back_thickness_mm = drawer.sizing.front_back_thickness_mm
        inside_right_mm = side_thickness_mm + drawer.clear_inside_width_mm
        inside_back_mm = drawer.side_length_mm - front_back_thickness_mm
        placements = {
            "left_side": DrawerPartPlacement(
                (side_thickness_mm, drawer.side_length_mm, 0.0),
                (0.0, -1.0, 0.0),
                (-1.0, 0.0, 0.0),
            ),
            "right_side": DrawerPartPlacement(
                (inside_right_mm, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (1.0, 0.0, 0.0),
            ),
            "front": DrawerPartPlacement(
                (side_thickness_mm, front_back_thickness_mm, 0.0),
                (1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
            ),
            "back": DrawerPartPlacement(
                (inside_right_mm, inside_back_mm, 0.0),
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
            ),
            "bottom": DrawerPartPlacement(
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


__all__ = ["DrawerPartLocator", "DrawerPartPlacement", "Vector3D"]
