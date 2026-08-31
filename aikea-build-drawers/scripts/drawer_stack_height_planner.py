"""Scope: Calculate useful drawer-box heights within fixed vertical boundaries."""

from __future__ import annotations

from dataclasses import dataclass


class DrawerStackHeightPlanningError(ValueError):
    """Report a drawer stack that cannot fit inside its supplied boundaries."""


@dataclass(frozen=True, slots=True)
class DrawerStackHeightRequest:
    """Describe one drawer bottom and any client-fixed box height."""

    drawer_id: str
    bottom_height_mm: float
    fixed_height_mm: float | None = None


@dataclass(frozen=True, slots=True)
class PlannedDrawerHeight:
    """Keep one resolved box height and its resulting clear space together."""

    drawer_id: str
    bottom_height_mm: float
    box_height_mm: float
    clear_gap_above_mm: float


@dataclass(frozen=True, slots=True)
class DrawerStackHeightPlan:
    """Carry the calculated heights for one vertically ordered drawer stack."""

    drawers: tuple[PlannedDrawerHeight, ...]


class DrawerStackHeightPlanner:
    """Fill drawer slots while preserving a deliberate clear gap above each box."""

    def plan(
        self,
        requests: tuple[DrawerStackHeightRequest, ...],
        *,
        top_boundary_mm: float,
        preferred_clear_gap_mm: float = 22.0,
        equalize_automatic_heights: bool = False,
    ) -> DrawerStackHeightPlan:
        ordered = tuple(sorted(requests, key=lambda item: item.bottom_height_mm))
        self._require_valid_inputs(ordered, top_boundary_mm, preferred_clear_gap_mm)
        upper_boundaries = tuple(
            item.bottom_height_mm for item in ordered[1:]
        ) + (top_boundary_mm,)
        automatic_capacities = tuple(
            upper - request.bottom_height_mm - preferred_clear_gap_mm
            for request, upper in zip(ordered, upper_boundaries)
            if request.fixed_height_mm is None
        )
        shared_height_mm = (
            min(automatic_capacities)
            if equalize_automatic_heights and automatic_capacities
            else None
        )
        planned = tuple(
            self._plan_drawer(
                request,
                upper,
                preferred_clear_gap_mm,
                shared_height_mm,
            )
            for request, upper in zip(ordered, upper_boundaries)
        )
        return DrawerStackHeightPlan(planned)

    def _require_valid_inputs(
        self,
        requests: tuple[DrawerStackHeightRequest, ...],
        top_boundary_mm: float,
        preferred_clear_gap_mm: float,
    ) -> None:
        ids = tuple(item.drawer_id for item in requests)
        bottoms = tuple(item.bottom_height_mm for item in requests)
        problems = tuple(
            message
            for condition, message in (
                (not requests, "a drawer stack cannot be empty"),
                (len(set(ids)) != len(ids), "drawer IDs must be unique"),
                (len(set(bottoms)) != len(bottoms), "drawer bottoms must be unique"),
                (preferred_clear_gap_mm < 0.0, "clear gap cannot be negative"),
                (
                    bool(requests) and top_boundary_mm <= max(bottoms),
                    "top boundary must sit above every drawer bottom",
                ),
            )
            if condition
        )
        if problems:
            raise DrawerStackHeightPlanningError("; ".join(problems))

    def _plan_drawer(
        self,
        request: DrawerStackHeightRequest,
        upper_boundary_mm: float,
        preferred_clear_gap_mm: float,
        shared_height_mm: float | None,
    ) -> PlannedDrawerHeight:
        available_height_mm = upper_boundary_mm - request.bottom_height_mm
        automatic_height_mm = available_height_mm - preferred_clear_gap_mm
        box_height_mm = (
            request.fixed_height_mm
            if request.fixed_height_mm is not None
            else shared_height_mm or automatic_height_mm
        )
        clear_gap_mm = available_height_mm - box_height_mm
        if box_height_mm <= 0.0 or clear_gap_mm < 0.0:
            raise DrawerStackHeightPlanningError(
                f"{request.drawer_id} cannot fit below its next boundary"
            )
        return PlannedDrawerHeight(
            request.drawer_id,
            request.bottom_height_mm,
            box_height_mm,
            clear_gap_mm,
        )


__all__ = [
    "DrawerStackHeightPlan",
    "DrawerStackHeightPlanner",
    "DrawerStackHeightPlanningError",
    "DrawerStackHeightRequest",
    "PlannedDrawerHeight",
]
