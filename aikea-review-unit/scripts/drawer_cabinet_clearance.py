"""Scope: Measure drawer clearances and material collisions inside one cabinet."""

from __future__ import annotations

from typing import Any

from placed_bounds import PlacedBounds


class DrawerCabinetClearance:
    """Calculate reusable physical evidence from already-placed review parts."""

    _TOLERANCE_MM = 1e-6

    def inner_bounds(self, cabinet: Any) -> PlacedBounds:
        left_mm = float(cabinet.part("left_side").local_size_mm[2])
        right_mm = float(cabinet.part("right_side").local_size_mm[2])
        shelf_bottoms = (
            float(dict(part.dimensions_mm)["bottom_height"])
            for part in cabinet.parts
            if part.role == "shelf_panel"
        )
        top_mm = float(cabinet.base_height_mm) + min(
            shelf_bottoms,
            default=min(point.height_mm for point in cabinet.top),
        )
        return PlacedBounds(
            left_mm,
            float(cabinet.width_mm) - right_mm,
            0.0,
            float(cabinet.inside_depth_mm),
            float(cabinet.base_height_mm),
            top_mm,
        )

    def contains(self, outer: PlacedBounds, inner: PlacedBounds) -> bool:
        minimums_fit = all(
            outer_value - self._TOLERANCE_MM <= inner_value
            for outer_value, inner_value in zip(
                (outer.x_min_mm, outer.y_min_mm, outer.z_min_mm),
                (inner.x_min_mm, inner.y_min_mm, inner.z_min_mm),
            )
        )
        maximums_fit = all(
            outer_value + self._TOLERANCE_MM >= inner_value
            for outer_value, inner_value in zip(
                (outer.x_max_mm, outer.y_max_mm, outer.z_max_mm),
                (inner.x_max_mm, inner.y_max_mm, inner.z_max_mm),
            )
        )
        return minimums_fit and maximums_fit

    def collisions(
        self,
        cabinet_parts: tuple[Any, ...],
        drawer_parts: tuple[Any, ...],
    ) -> tuple[tuple[str, str], ...]:
        return tuple(
            (cabinet_part.name, drawer_part.name)
            for cabinet_part in cabinet_parts
            for drawer_part in drawer_parts
            if cabinet_part.placed_shape()
            .intersect(drawer_part.placed_shape())
            .Volume()
            > self._TOLERANCE_MM
        )

    def clearances(
        self,
        outer: PlacedBounds,
        inner: PlacedBounds,
    ) -> dict[str, float]:
        return {
            "left": inner.x_min_mm - outer.x_min_mm,
            "right": outer.x_max_mm - inner.x_max_mm,
            "front": inner.y_min_mm - outer.y_min_mm,
            "rear": outer.y_max_mm - inner.y_max_mm,
            "below": inner.z_min_mm - outer.z_min_mm,
            "above": outer.z_max_mm - inner.z_max_mm,
        }

    def part_positions(
        self,
        parts: tuple[Any, ...],
        global_offset: tuple[float, float, float],
    ) -> dict[str, Any]:
        return {
            part.name: {
                "cabinet_bounds": PlacedBounds.from_parts((part,)).as_dict(),
                "global_bounds": PlacedBounds.from_parts((part,))
                .shifted(global_offset)
                .as_dict(),
            }
            for part in parts
        }


__all__ = ["DrawerCabinetClearance"]
