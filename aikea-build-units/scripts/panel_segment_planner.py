"""Scope: Divide one rectangular panel span into CNC-sized manufacturable segments."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import ceil

from cnc_work_area import CncWorkArea


@dataclass(frozen=True)
class PanelSegment:
    """Describe one ordered interval along the panel's segmented axis."""

    index: int
    start_mm: float
    end_mm: float

    @property
    def length_mm(self) -> float:
        return self.end_mm - self.start_mm


class PanelSegmentPlanner:
    """Use the fewest segments while preferring supplied structural boundaries."""

    def __init__(self, work_area: CncWorkArea) -> None:
        self.work_area = work_area

    def plan(
        self,
        span_mm: float,
        transverse_size_mm: float,
        preferred_breaks_mm: tuple[float, ...] = (),
    ) -> tuple[PanelSegment, ...]:
        if span_mm <= 0 or transverse_size_mm <= 0:
            raise ValueError("panel dimensions must be greater than zero")
        maximum_span_mm = self.work_area.maximum_span_mm(transverse_size_mm)
        segment_count = ceil(span_mm / maximum_span_mm)
        if segment_count == 1:
            return (PanelSegment(1, 0.0, span_mm),)
        breaks = self._preferred_breaks(
            span_mm,
            maximum_span_mm,
            segment_count,
            preferred_breaks_mm,
        )
        if breaks is None:
            segment_length_mm = span_mm / segment_count
            breaks = tuple(
                segment_length_mm * index
                for index in range(1, segment_count)
            )
        points = (0.0, *breaks, span_mm)
        return tuple(
            PanelSegment(index, start, end)
            for index, (start, end) in enumerate(zip(points, points[1:]), start=1)
        )

    def _preferred_breaks(
        self,
        span_mm: float,
        maximum_span_mm: float,
        segment_count: int,
        preferred_breaks_mm: tuple[float, ...],
    ) -> tuple[float, ...] | None:
        candidates = tuple(
            sorted({position for position in preferred_breaks_mm if 0 < position < span_mm})
        )
        valid = tuple(
            breaks
            for breaks in combinations(candidates, segment_count - 1)
            if self._longest_segment_mm(span_mm, breaks) <= maximum_span_mm
        )
        if not valid:
            return None
        ideal_length_mm = span_mm / segment_count
        return min(
            valid,
            key=lambda breaks: (
                max(
                    abs(length - ideal_length_mm)
                    for length in self._segment_lengths(span_mm, breaks)
                ),
                breaks,
            ),
        )

    def _longest_segment_mm(
        self,
        span_mm: float,
        breaks: tuple[float, ...],
    ) -> float:
        return max(self._segment_lengths(span_mm, breaks))

    def _segment_lengths(
        self,
        span_mm: float,
        breaks: tuple[float, ...],
    ) -> tuple[float, ...]:
        points = (0.0, *breaks, span_mm)
        return tuple(end - start for start, end in zip(points, points[1:]))


__all__ = ["PanelSegment", "PanelSegmentPlanner"]
