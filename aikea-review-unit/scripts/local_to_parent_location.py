"""Scope: Convert one explicit assembly frame into a CadQuery location."""

from __future__ import annotations

from typing import Any

import cadquery as cq


class AssemblyFrameError(ValueError):
    """Report a declared basis that cannot represent a rigid right-handed frame."""


class LocalToParentLocation:
    """Preserve a declared origin and axes when entering CadQuery geometry."""

    def build(self, placement: Any) -> cq.Location:
        origin = placement.origin_in_parent
        axes = placement.axis_basis
        local_x = self._vector(axes.local_x_in_parent)
        local_y = self._vector(axes.local_y_in_parent)
        local_z = self._vector(axes.local_z_in_parent)
        self._require_right_handed_basis(local_x, local_y, local_z)
        return cq.Location(
            cq.Plane(
                origin=(origin.x_mm, origin.y_mm, origin.z_mm),
                xDir=local_x,
                normal=local_z,
            )
        )

    def _vector(self, direction: Any) -> tuple[float, float, float]:
        return direction.x, direction.y, direction.z

    def _require_right_handed_basis(
        self,
        x_axis: tuple[float, float, float],
        y_axis: tuple[float, float, float],
        z_axis: tuple[float, float, float],
    ) -> None:
        vectors = tuple(cq.Vector(*axis) for axis in (x_axis, y_axis, z_axis))
        lengths_are_one = all(abs(vector.Length - 1.0) <= 1e-9 for vector in vectors)
        axes_are_orthogonal = all(
            abs(left.dot(right)) <= 1e-9
            for left, right in (
                (vectors[0], vectors[1]),
                (vectors[0], vectors[2]),
                (vectors[1], vectors[2]),
            )
        )
        derived_z = vectors[0].cross(vectors[1])
        is_right_handed = derived_z.sub(vectors[2]).Length <= 1e-9
        if not (lengths_are_one and axes_are_orthogonal and is_right_handed):
            raise AssemblyFrameError(
                "local-to-parent axes must form an orthonormal right-handed basis"
            )


__all__ = ["AssemblyFrameError", "LocalToParentLocation"]
