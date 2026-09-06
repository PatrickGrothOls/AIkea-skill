"""Scope: Verify oversize rectangular panels become ordered CNC-sized segments."""

from cnc_work_area import CNC_2500_X_2000_8MM
from panel_segment_planner import PanelSegmentPlanner


class TestPanelSegmentPlanner:
    """Keep segmentation minimal, manufacturable, and structurally aligned."""

    def setup_method(self) -> None:
        self.planner = PanelSegmentPlanner(CNC_2500_X_2000_8MM)

    def test_panel_inside_the_work_area_remains_whole(self) -> None:
        segments = self.planner.plan(991.333333, 582.0)

        assert [(item.start_mm, item.end_mm) for item in segments] == [
            (0.0, 991.333333)
        ]

    def test_wardrobe_width_prefers_a_cabinet_boundary(self) -> None:
        segments = self.planner.plan(
            2978.0,
            582.0,
            (992.333333, 1985.666667),
        )

        assert len(segments) == 2
        assert segments[0].end_mm == 992.333333
        assert segments[1].start_mm == 992.333333
        assert all(item.length_mm <= 2496.0 for item in segments)

    def test_run_without_a_supported_boundary_splits_evenly(self) -> None:
        segments = self.planner.plan(6000.0, 582.0)

        assert [item.length_mm for item in segments] == [2000.0, 2000.0, 2000.0]
        assert [item.index for item in segments] == [1, 2, 3]
