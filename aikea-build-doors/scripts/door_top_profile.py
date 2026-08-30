"""Scope: Read and sample the manufactured top edge of one shaped door."""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any


@dataclass(frozen=True, slots=True)
class DoorTopPoint:
    x_mm: float
    height_mm: float


class DoorTopProfile:
    """Expose the door top as ordered linear segments in its panel frame."""

    def __init__(self, points: tuple[DoorTopPoint, ...]) -> None:
        self.points = points

    @classmethod
    def from_part(cls, part: Any) -> DoorTopProfile:
        dimensions = {name: float(value) for name, value in part.dimensions_mm}
        heights_by_x: dict[float, float] = {}
        for point in part.outline_mm:
            x_mm = float(point.x_mm)
            heights_by_x[x_mm] = max(
                heights_by_x.get(x_mm, 0.0),
                float(point.height_mm),
            )
        if not heights_by_x:
            heights_by_x = {
                0.0: dimensions["left_height"],
                dimensions["width"]: dimensions["right_height"],
            }
        return cls(
            tuple(
                DoorTopPoint(x_mm, height_mm)
                for x_mm, height_mm in sorted(heights_by_x.items())
            )
        )

    @property
    def maximum_slope(self) -> float:
        return max(
            (
                abs(right.height_mm - left.height_mm)
                / (right.x_mm - left.x_mm)
                for left, right in zip(self.points, self.points[1:])
            ),
            default=0.0,
        )

    def samples(self, maximum_step_mm: float) -> tuple[DoorTopPoint, ...]:
        samples: list[DoorTopPoint] = []
        for left, right in zip(self.points, self.points[1:]):
            count = max(1, ceil((right.x_mm - left.x_mm) / maximum_step_mm))
            for index in range(count):
                fraction = index / count
                samples.append(
                    DoorTopPoint(
                        left.x_mm + (right.x_mm - left.x_mm) * fraction,
                        left.height_mm
                        + (right.height_mm - left.height_mm) * fraction,
                    )
                )
        samples.append(self.points[-1])
        return tuple(samples)


__all__ = ["DoorTopPoint", "DoorTopProfile"]
