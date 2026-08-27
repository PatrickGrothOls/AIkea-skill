"""Scope: Divide one structural base into CNC-sized modules at useful run boundaries."""

from __future__ import annotations

from assembly_taxonomy import BaseModuleTaxonomy
from cnc_work_area import CncWorkArea
from panel_segment_planner import PanelSegmentPlanner


class BaseModulePlanner:
    """Prefer cabinet gaps while keeping every deck and rail segment manufacturable."""

    def __init__(self, work_area: CncWorkArea) -> None:
        self.segment_planner = PanelSegmentPlanner(work_area)

    def plan(
        self,
        cabinet_spans_mm: tuple[tuple[float, float], ...],
        depth_mm: float,
    ) -> tuple[BaseModuleTaxonomy, ...]:
        if not cabinet_spans_mm:
            raise ValueError("base planning requires at least one cabinet span")
        global_left_mm = cabinet_spans_mm[0][0]
        global_right_mm = cabinet_spans_mm[-1][1]
        width_mm = global_right_mm - global_left_mm
        preferred_breaks_mm = tuple(
            ((left_span[1] + right_span[0]) / 2.0) - global_left_mm
            for left_span, right_span in zip(
                cabinet_spans_mm,
                cabinet_spans_mm[1:],
            )
        )
        segments = self.segment_planner.plan(
            width_mm,
            depth_mm,
            preferred_breaks_mm,
        )
        return tuple(
            BaseModuleTaxonomy(
                f"base_module_{segment.index:02d}",
                segment.start_mm,
                segment.end_mm,
            )
            for segment in segments
        )


__all__ = ["BaseModulePlanner"]
