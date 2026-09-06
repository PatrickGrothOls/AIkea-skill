"""Scope: Report every physical part's local-to-assembly-to-global placement."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from assembly_part_locator import AssemblyPartLocator
from base_part_locator import BasePartLocator


class PhysicalPartPositionReporter:
    """Expose each part zero and axis without changing its manufactured solid."""

    def __init__(self) -> None:
        self.cabinet_locator = AssemblyPartLocator()
        self.base_locator = BasePartLocator()

    def cabinet_positions(self, built_cabinet: Any) -> dict[str, Any]:
        spec = built_cabinet.spec
        return {
            part.spec.part_id: self._values(
                part,
                self.cabinet_locator.locate(
                    part.spec,
                    spec,
                    float(spec.base_height_mm),
                ),
                float(spec.global_left_mm),
            )
            for part in built_cabinet.parts
        }

    def base_positions(self, built_base: Any) -> dict[str, Any]:
        spec = built_base.spec
        return {
            part.spec.part_id: self._values(
                part,
                self.base_locator.locate(part.spec, spec),
                float(spec.global_left_mm),
            )
            for part in built_base.parts
        }

    def _values(
        self,
        built_part: Any,
        location: cq.Location,
        assembly_global_x_mm: float,
    ) -> dict[str, Any]:
        matrix = cq.Matrix(location.wrapped.Transformation())
        assembly_zero = cq.Vector(0.0, 0.0, 0.0).transform(matrix)
        axes = {
            name: self._direction(vector, matrix, assembly_zero)
            for name, vector in {
                "x": cq.Vector(1.0, 0.0, 0.0),
                "y": cq.Vector(0.0, 1.0, 0.0),
                "z": cq.Vector(0.0, 0.0, 1.0),
            }.items()
        }
        assembly_bounds = built_part.solid.val().located(location).BoundingBox()
        return {
            "role": built_part.spec.role,
            "local_zero_mm": [0.0, 0.0, 0.0],
            "assembly_zero_mm": self._vector_values(assembly_zero),
            "global_zero_mm": [
                assembly_zero.x + assembly_global_x_mm,
                assembly_zero.y,
                assembly_zero.z,
            ],
            "local_axes_in_assembly": axes,
            "assembly_bounds": self._bounds_values(assembly_bounds),
            "global_bounds": self._bounds_values(
                assembly_bounds,
                assembly_global_x_mm,
            ),
        }

    def _direction(
        self,
        local_axis: cq.Vector,
        matrix: cq.Matrix,
        assembly_zero: cq.Vector,
    ) -> list[float]:
        endpoint = local_axis.transform(matrix)
        return self._vector_values(endpoint - assembly_zero)

    def _vector_values(self, vector: cq.Vector) -> list[float]:
        return [self._clean(vector.x), self._clean(vector.y), self._clean(vector.z)]

    def _bounds_values(
        self,
        bounds: Any,
        global_x_offset_mm: float = 0.0,
    ) -> dict[str, list[float]]:
        return {
            "minimum_mm": [
                self._clean(bounds.xmin + global_x_offset_mm),
                self._clean(bounds.ymin),
                self._clean(bounds.zmin),
            ],
            "maximum_mm": [
                self._clean(bounds.xmax + global_x_offset_mm),
                self._clean(bounds.ymax),
                self._clean(bounds.zmax),
            ],
        }

    def _clean(self, value: float) -> float:
        return 0.0 if abs(value) < 1e-9 else float(value)


__all__ = ["PhysicalPartPositionReporter"]
