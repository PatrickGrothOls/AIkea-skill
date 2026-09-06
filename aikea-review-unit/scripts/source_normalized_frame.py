"""Scope: Map exact source geometry into its installed assembly frame."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Any, ClassVar


@dataclass(frozen=True, slots=True)
class SourceNormalizedFrame:
    """Remove a source shape's stored location before comparing installations."""

    part: Any
    source: Any
    _BASIS_POINTS: ClassVar[tuple[tuple[float, ...], ...]] = (
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )

    def point(self, source_point: tuple[float, ...]) -> tuple[float, ...]:
        import cadquery as cq

        source_to_world = self.part.location * self.source.location().inverse
        matrix = cq.Matrix(source_to_world.wrapped.Transformation())
        transformed = cq.Vector(*source_point).transform(matrix)
        return tuple(float(value) for value in transformed.toTuple())

    def translated_matches(
        self,
        other: "SourceNormalizedFrame",
        offset: tuple[float, ...],
        tolerance_mm: float,
    ) -> bool:
        return all(
            self._same(
                tuple(
                    value + delta
                    for value, delta in zip(self.point(point), offset)
                ),
                other.point(point),
                tolerance_mm,
            )
            for point in self._BASIS_POINTS
        )

    def unit_direction(
        self,
        start: tuple[float, ...],
        end: tuple[float, ...],
    ) -> tuple[float, ...]:
        start_point = self.point(start)
        end_point = self.point(end)
        values = tuple(right - left for left, right in zip(start_point, end_point))
        length = sqrt(sum(value * value for value in values))
        return tuple(value / length for value in values)

    def _same(
        self,
        left: tuple[float, ...],
        right: tuple[float, ...],
        tolerance_mm: float,
    ) -> bool:
        return all(
            abs(left_value - right_value) <= tolerance_mm
            for left_value, right_value in zip(left, right)
        )


__all__ = ["SourceNormalizedFrame"]
