"""Scope: Verify cutter clearance and orientation against the CNC working area."""

from cnc_work_area import CNC_2500_X_2000_8MM, CncWorkAreaError


class TestCncWorkArea:
    """Protect the agreed machine travel and cutter-radius calculation."""

    def test_usable_axes_subtract_the_cutter_radius(self) -> None:
        assert CNC_2500_X_2000_8MM.usable_x_mm == 2496.0
        assert CNC_2500_X_2000_8MM.usable_y_mm == 1996.0

    def test_panel_may_rotate_to_use_the_long_axis(self) -> None:
        assert CNC_2500_X_2000_8MM.fits(2400.0, 1000.0)
        assert CNC_2500_X_2000_8MM.fits(1000.0, 2400.0)
        assert not CNC_2500_X_2000_8MM.fits(2497.0, 1997.0)

    def test_maximum_span_depends_on_the_transverse_dimension(self) -> None:
        assert CNC_2500_X_2000_8MM.maximum_span_mm(582.0) == 2496.0
        assert CNC_2500_X_2000_8MM.maximum_span_mm(2100.0) == 1996.0

    def test_part_wider_than_both_axes_is_rejected(self) -> None:
        try:
            CNC_2500_X_2000_8MM.maximum_span_mm(2500.0)
        except CncWorkAreaError as error:
            assert "exceeds both usable CNC axes" in str(error)
        else:
            raise AssertionError("oversize transverse dimension was accepted")
