"""Scope: Produce opposite cutters for two panels sharing one true miter plane."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq
import numpy as np


_CUTTER_SIZE_MM = 5000.0
_PARALLEL_EPS = 1e-6


@dataclass(frozen=True)
class MiterEdgeMate:
    """Snapshot the shared bisecting plane before either participant is cut."""

    plane_origin: tuple[float, float, float]
    plane_normal: tuple[float, float, float]

    @classmethod
    def from_planes(
        cls,
        point_a: cq.Vector,
        normal_a: cq.Vector,
        point_b: cq.Vector,
        normal_b: cq.Vector,
    ) -> "MiterEdgeMate":
        """Resolve the correct bisector from face centers as well as normals."""
        center_a = cq.Vector(point_a.x, point_a.y, point_a.z)
        center_b = cq.Vector(point_b.x, point_b.y, point_b.z)
        face_normal_a = normal_a.normalized()
        face_normal_b = normal_b.normalized()
        edge_vector = face_normal_a.cross(face_normal_b)
        if edge_vector.Length < _PARALLEL_EPS:
            raise ValueError("miter outside-face planes are parallel")
        edge_direction = edge_vector.normalized()

        midpoint = (center_a + center_b) * 0.5
        matrix = np.array(
            [
                [face_normal_a.x, face_normal_a.y, face_normal_a.z],
                [face_normal_b.x, face_normal_b.y, face_normal_b.z],
                [edge_direction.x, edge_direction.y, edge_direction.z],
            ]
        )
        right_hand_side = np.array(
            [
                face_normal_a.dot(center_a),
                face_normal_b.dot(center_b),
                edge_direction.dot(midpoint),
            ]
        )
        solved = np.linalg.solve(matrix, right_hand_side)
        origin = cq.Vector(*(float(value) for value in solved))

        direction_a = cls._face_direction(center_a, origin, edge_direction)
        direction_b = cls._face_direction(center_b, origin, edge_direction)
        miter_normal = (direction_b - direction_a).normalized()
        return cls(
            (origin.x, origin.y, origin.z),
            (miter_normal.x, miter_normal.y, miter_normal.z),
        )

    def cutter_for_a(self) -> cq.Shape:
        """Remove the positive half-space so panel A keeps the negative side."""
        return self._half_space_cutter(remove_positive=True).val()

    def cutter_for_b(self) -> cq.Shape:
        """Remove the negative half-space so panel B keeps the positive side."""
        return self._half_space_cutter(remove_positive=False).val()

    @staticmethod
    def _face_direction(
        center: cq.Vector,
        origin: cq.Vector,
        edge_direction: cq.Vector,
    ) -> cq.Vector:
        offset = center - origin
        return (offset - edge_direction * offset.dot(edge_direction)).normalized()

    def _half_space_cutter(self, *, remove_positive: bool) -> cq.Workplane:
        size_mm = _CUTTER_SIZE_MM
        normal = cq.Vector(*self.plane_normal).normalized()
        reference = (
            cq.Vector(0.0, 0.0, 1.0)
            if abs(normal.z) < 0.9
            else cq.Vector(1.0, 0.0, 0.0)
        )
        x_direction = normal.cross(reference).normalized()
        plane = cq.Plane(
            origin=self.plane_origin,
            xDir=(x_direction.x, x_direction.y, x_direction.z),
            normal=(normal.x, normal.y, normal.z),
        )
        distance_mm = size_mm if remove_positive else -size_mm
        return cq.Workplane(plane).rect(size_mm * 2.0, size_mm * 2.0).extrude(distance_mm)


__all__ = ["MiterEdgeMate"]
