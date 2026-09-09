"""Scope: Verify cutter clearance and orientation against the CNC working area."""

import pytest

from cnc_work_area import CNC_2500_X_2000_8MM, CncWorkArea, CncWorkAreaError


class TestCncWorkArea:
    """Protect the agreed machine travel and 2490 mm limit and two-sided cutter clearance."""

    def test_usable_axes_reserve_full_cutter_and_edge_margins(self) -> None:
        assert CNC_2500_X_2000_8MM.usable_x_mm == 2490.0
        assert CNC_2500_X_2000_8MM.usable_y_mm == 1990.0

    def test_panel_may_rotate_to_use_the_long_axis(self) -> None:
        assert CNC_2500_X_2000_8MM.fits(2400.0, 1000.0)
        assert CNC_2500_X_2000_8MM.fits(1000.0, 2400.0)
        assert not CNC_2500_X_2000_8MM.fits(2497.0, 1997.0)

    def test_2490_is_allowed_but_any_larger_panel_is_not(self) -> None:
        assert CNC_2500_X_2000_8MM.fits(2490, 1990)
        assert CNC_2500_X_2000_8MM.fits(1990, 2490)
        assert not CNC_2500_X_2000_8MM.fits(2490.001, 100)
        assert not CNC_2500_X_2000_8MM.fits(100, 2496)

    def test_other_profiles_reserve_both_sides_of_their_actual_tool(self) -> None:
        profile = CncWorkArea("small", 1000, 600, 10)
        assert (profile.usable_x_mm, profile.usable_y_mm) == (990, 590)
        with pytest.raises(ValueError, match="usable CNC area"):
            CncWorkArea("unusable", 10, 10, 8, edge_margin_mm=1)

    def test_maximum_span_depends_on_the_transverse_dimension(self) -> None:
        assert CNC_2500_X_2000_8MM.maximum_span_mm(582.0) == 2490.0
        assert CNC_2500_X_2000_8MM.maximum_span_mm(2100.0) == 1990.0

    def test_part_wider_than_both_axes_is_rejected(self) -> None:
        try:
            CNC_2500_X_2000_8MM.maximum_span_mm(2500.0)
        except CncWorkAreaError as error:
            assert "exceeds both usable CNC axes" in str(error)
        else:
            raise AssertionError("oversize transverse dimension was accepted")
