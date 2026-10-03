"""Scope: Verify panel outlines keep only meaningful top-boundary vertices."""

from assembly_taxonomy import BoundaryPoint
from top_boundary_panel_outline_builder import TopBoundaryPanelOutlineBuilder


class TestTopBoundaryPanelOutlineBuilder:
    """Protect local outlines from floating-point duplicate endpoints."""

    def test_nearly_equal_right_endpoint_is_written_once(self) -> None:
        top = (
            BoundaryPoint(0.0, 2284.0),
            BoundaryPoint(991.3333333333333, 2284.0),
        )

        outline = TopBoundaryPanelOutlineBuilder().build(
            top,
            0.0,
            991.3333333333334,
        )

        assert outline == (
            BoundaryPoint(0.0, 0.0),
            BoundaryPoint(991.3333333333334, 0.0),
            BoundaryPoint(991.3333333333334, 2284.0),
            BoundaryPoint(0.0, 2284.0),
        )

    def test_real_internal_boundary_change_is_preserved(self) -> None:
        top = (
            BoundaryPoint(0.0, 2400.0),
            BoundaryPoint(400.0, 2400.0),
            BoundaryPoint(1000.0, 1800.0),
        )

        outline = TopBoundaryPanelOutlineBuilder().build(top, 0.0, 1000.0)

        assert BoundaryPoint(400.0, 2400.0) in outline
