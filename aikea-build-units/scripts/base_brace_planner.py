"""Scope: Position full-height braces inside one structural base module."""

from __future__ import annotations

from math import ceil


class BaseBracePlanner:
    """Support both module ends and keep every internal brace interval bounded."""

    def positions_mm(
        self,
        module_width_mm: float,
        brace_thickness_mm: float,
        maximum_spacing_mm: float,
    ) -> tuple[float, ...]:
        clear_center_span_mm = module_width_mm - brace_thickness_mm
        if clear_center_span_mm < 0:
            raise ValueError("base module is narrower than one brace")
        if clear_center_span_mm == 0:
            return (module_width_mm / 2.0,)
        interval_count = ceil(clear_center_span_mm / maximum_spacing_mm)
        interval_mm = clear_center_span_mm / interval_count
        first_center_mm = brace_thickness_mm / 2.0
        return tuple(
            first_center_mm + (interval_mm * index)
            for index in range(interval_count + 1)
        )


__all__ = ["BaseBracePlanner"]
