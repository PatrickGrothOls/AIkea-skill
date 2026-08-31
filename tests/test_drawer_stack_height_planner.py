"""Scope: Verify drawer stacks use their vertical capacity deliberately."""

import pytest

from drawer_stack_height_planner import (
    DrawerStackHeightPlanner,
    DrawerStackHeightPlanningError,
    DrawerStackHeightRequest,
)


class TestDrawerStackHeightPlanner:
    """Protect calculated box heights across System 32 mounting intervals."""

    def setup_method(self) -> None:
        self.planner = DrawerStackHeightPlanner()

    def test_fills_six_row_intervals_with_a_deliberate_gap(self) -> None:
        plan = self.planner.plan(
            (
                DrawerStackHeightRequest("drawer_01", 177.0),
                DrawerStackHeightRequest("drawer_02", 369.0),
                DrawerStackHeightRequest("drawer_03", 561.0),
            ),
            top_boundary_mm=753.0,
        )

        assert tuple(item.box_height_mm for item in plan.drawers) == (
            170.0,
            170.0,
            170.0,
        )
        assert tuple(item.clear_gap_above_mm for item in plan.drawers) == (
            22.0,
            22.0,
            22.0,
        )

    def test_five_row_intervals_produce_shorter_boxes(self) -> None:
        plan = self.planner.plan(
            (
                DrawerStackHeightRequest("drawer_01", 177.0),
                DrawerStackHeightRequest("drawer_02", 337.0),
            ),
            top_boundary_mm=497.0,
        )

        assert tuple(item.box_height_mm for item in plan.drawers) == (138.0, 138.0)

    def test_preserves_a_client_fixed_height_and_reports_its_gap(self) -> None:
        plan = self.planner.plan(
            (
                DrawerStackHeightRequest("drawer_01", 177.0, fixed_height_mm=150.0),
                DrawerStackHeightRequest("drawer_02", 369.0),
            ),
            top_boundary_mm=561.0,
        )

        assert plan.drawers[0].box_height_mm == 150.0
        assert plan.drawers[0].clear_gap_above_mm == 42.0
        assert plan.drawers[1].box_height_mm == 170.0

    def test_can_equalize_a_matching_set_across_unequal_intervals(self) -> None:
        plan = self.planner.plan(
            (
                DrawerStackHeightRequest("drawer_01", 177.0),
                DrawerStackHeightRequest("drawer_02", 369.0),
            ),
            top_boundary_mm=593.0,
            equalize_automatic_heights=True,
        )

        assert tuple(item.box_height_mm for item in plan.drawers) == (170.0, 170.0)
        assert tuple(item.clear_gap_above_mm for item in plan.drawers) == (22.0, 54.0)

    def test_rejects_a_fixed_height_that_crosses_the_next_boundary(self) -> None:
        with pytest.raises(
            DrawerStackHeightPlanningError,
            match="drawer_01 cannot fit below its next boundary",
        ):
            self.planner.plan(
                (DrawerStackHeightRequest("drawer_01", 177.0, fixed_height_mm=200.0),),
                top_boundary_mm=369.0,
            )
