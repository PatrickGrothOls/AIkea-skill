"""Scope: Convert one explicit assembly frame into a CadQuery location."""

from __future__ import annotations

from typing import Any

import cadquery as cq


class LocalToParentLocation:
    """Preserve a declared origin and axes when entering CadQuery geometry."""

    def build(self, placement: Any) -> cq.Location:
        origin = placement.origin_in_parent
        axes = placement.axis_basis
        local_x = self._vector(axes.local_x_in_parent)
        local_z = self._vector(axes.local_z_in_parent)
        return cq.Location(
            cq.Plane(
                origin=(origin.x_mm, origin.y_mm, origin.z_mm),
                xDir=local_x,
                normal=local_z,
            )
        )

    def _vector(self, direction: Any) -> tuple[float, float, float]:
        return direction.x, direction.y, direction.z

__all__ = ["LocalToParentLocation"]
