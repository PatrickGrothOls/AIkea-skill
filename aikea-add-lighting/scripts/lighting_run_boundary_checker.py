"""Scope: Check whether a recessed-light run stays inside its host face."""

from __future__ import annotations

from lighting_run import LightingRun


class LightingRunBoundaryChecker:
    """Include the full groove width when checking the two run endpoints."""

    def is_inside(
        self,
        face_width_mm: float,
        face_height_mm: float,
        run: LightingRun,
    ) -> bool:
        dx = (run.end_mm[0] - run.start_mm[0]) / run.length_mm
        dy = (run.end_mm[1] - run.start_mm[1]) / run.length_mm
        offset = run.profile.groove_width_mm / 2.0
        perpendicular = (-dy * offset, dx * offset)
        corners = tuple(
            (point[0] + side * perpendicular[0], point[1] + side * perpendicular[1])
            for point in (run.start_mm, run.end_mm)
            for side in (-1.0, 1.0)
        )
        return all(
            0.0 <= x <= face_width_mm and 0.0 <= y <= face_height_mm
            for x, y in corners
        )


__all__ = ["LightingRunBoundaryChecker"]
