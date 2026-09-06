"""Scope: Convert one explicit assembly frame into a CadQuery location."""

from __future__ import annotations

from typing import Any

import cadquery as cq


class LocalToParentLocation:
    """Preserve a declared origin and axes when entering CadQuery geometry."""

    def build(self, placement: Any) -> cq.Location:
        origin = placement.origin_in_parent
        axes = placement.axis_basis
        return cq.Location(
            cq.Plane(
                origin=(origin.x_mm, origin.y_mm, origin.z_mm),
                xDir=self._vector(axes.local_x_in_parent),
                normal=self._vector(axes.local_z_in_parent),
            )
        )

    def _vector(self, direction: Any) -> tuple[float, float, float]:
        return direction.x, direction.y, direction.z


__all__ = ["LocalToParentLocation"]
