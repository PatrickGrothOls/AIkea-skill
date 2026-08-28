"""Scope: Recognize the official lower-rear drawer preparation zone."""

from __future__ import annotations

from typing import Any


class RunnerBackPreparationZone:
    """Admit only runner/back overlap at the back's lower rear edge."""

    _TOLERANCE_MM = 1e-6
    _HEIGHT_MM = 13.0

    def contains(
        self,
        hardware_id: str,
        wood_id: str,
        hardware_shape: Any,
        wood_shape: Any,
    ) -> bool:
        if not hardware_id.startswith("runner_") or not wood_id.endswith("__back"):
            return False
        overlap_bounds = hardware_shape.intersect(wood_shape).BoundingBox()
        wood_bounds = wood_shape.BoundingBox()
        reaches_lower_rear_edge = (
            abs(overlap_bounds.ymax - wood_bounds.ymax) <= self._TOLERANCE_MM,
            abs(overlap_bounds.zmin - wood_bounds.zmin) <= self._TOLERANCE_MM,
            overlap_bounds.zmax
            <= wood_bounds.zmin + self._HEIGHT_MM + self._TOLERANCE_MM,
        )
        return all(reaches_lower_rear_edge)


__all__ = ["RunnerBackPreparationZone"]
