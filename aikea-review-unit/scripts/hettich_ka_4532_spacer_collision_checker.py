"""Scope: Find unintended exact and swept KA 4532 drawer conflicts."""

from __future__ import annotations

from typing import Any

from drawer_hardware_overlap_checker import DrawerHardwareOverlapChecker


class HettichKa4532SpacerCollisionChecker:
    """Check endpoints exactly and the complete linear travel conservatively."""

    _TOLERANCE_MM = 1e-6

    def __init__(self) -> None:
        self.overlaps = DrawerHardwareOverlapChecker()

    def check(
        self,
        drawer_id: str,
        closed: dict[str, Any],
        opened: dict[str, Any],
        moving_names: tuple[str, ...],
        static_names: tuple[str, ...],
    ) -> dict[str, Any]:
        excluded = self._articulated_pairs(drawer_id)
        return {
            "method": "exact_endpoint_intersections_plus_linear_swept_aabb",
            "excluded_manufacturer_articulation_pairs": [list(pair) for pair in excluded],
            "closed_endpoint_pairs": [
                list(pair)
                for pair in self._endpoint_pairs(
                    closed, moving_names, static_names, excluded
                )
            ],
            "open_endpoint_pairs": [
                list(pair)
                for pair in self._endpoint_pairs(
                    opened, moving_names, static_names, excluded
                )
            ],
            "swept_envelope_pairs": [
                list(pair)
                for pair in self._swept_pairs(
                    closed,
                    opened,
                    moving_names,
                    static_names,
                    excluded,
                )
            ],
        }

    def _endpoint_pairs(self, parts, moving_names, static_names, excluded):
        return tuple(
            (moving, static)
            for moving in moving_names
            for static in static_names
            if (moving, static) not in excluded
            and self.overlaps.overlap(
                parts[moving].placed_shape(), parts[static].placed_shape()
            )
            > self._TOLERANCE_MM
        )

    def _swept_pairs(self, closed, opened, moving_names, static_names, excluded):
        return tuple(
            (moving, static)
            for moving in moving_names
            for static in static_names
            if (moving, static) not in excluded
            and self._bounds_overlap(
                self._swept_bounds(closed[moving], opened[moving]),
                self._shape_bounds(closed[static].placed_shape()),
            )
        )

    def _swept_bounds(self, closed: Any, opened: Any) -> tuple[float, ...]:
        left = self._shape_bounds(closed.placed_shape())
        right = self._shape_bounds(opened.placed_shape())
        return tuple(
            min(left[index], right[index])
            if index % 2 == 0
            else max(left[index], right[index])
            for index in range(6)
        )

    def _shape_bounds(self, shape: Any) -> tuple[float, ...]:
        bounds = shape.BoundingBox()
        return (
            bounds.xmin,
            bounds.xmax,
            bounds.ymin,
            bounds.ymax,
            bounds.zmin,
            bounds.zmax,
        )

    def _bounds_overlap(self, left: tuple[float, ...], right: tuple[float, ...]) -> bool:
        return all(
            left[index + 1] > right[index] + self._TOLERANCE_MM
            and right[index + 1] > left[index] + self._TOLERANCE_MM
            for index in (0, 2, 4)
        )

    def _articulated_pairs(self, drawer_id: str) -> tuple[tuple[str, str], ...]:
        return tuple(
            (
                f"{drawer_id}__{drawer_id}_runner_{hand}_moving",
                f"{drawer_id}_runner_{hand}_fixed",
            )
            for hand in ("left", "right")
        )


__all__ = ["HettichKa4532SpacerCollisionChecker"]
