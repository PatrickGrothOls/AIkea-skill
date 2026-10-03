"""Scope: Verify sourced MOVENTO planning values and depth selection."""

import pytest

from movento_runner_catalog import (
    MOVENTO_760H5000S,
    MOVENTO_760H5500S,
    MOVENTO_RUNNER_CATALOG,
    MoventoRunnerSelectionError,
)


class TestMoventoRunnerProfile:
    """Protect the hardware-owned dimensions used by drawer planning."""

    def test_500_profile_keeps_its_verified_product_dimensions(self) -> None:
        profile = MOVENTO_760H5000S

        assert profile.product_code == "760H5000S"
        assert profile.item_number == "05083446"
        assert profile.nominal_length_mm == 500.0
        assert profile.maximum_load_kg == 40.0
        assert profile.mounting_width_mm == 21.0
        assert profile.runner_bearing_height_mm == 28.5
        assert profile.cabinet_profile_width_mm == 40.9
        hardware = profile.hardware_asset_set
        assert hardware.runner_left.asset_id == (
            "movento-760h5000s-runner-left"
        )
        assert hardware.runner_right.asset_id == (
            "movento-760h5000s-runner-right"
        )
        assert hardware.locking_device_left.asset_id == (
            "t51-7601-left-locking-device"
        )
        assert hardware.locking_device_right.asset_id == (
            "t51-7601-right-locking-device"
        )

    def test_550_profile_does_not_invent_a_complete_hardware_set(self) -> None:
        assert MOVENTO_760H5500S.hardware_asset_set is None

    def test_drawer_dimensions_remain_hardware_owned(self) -> None:
        limits = MOVENTO_760H5000S.drawer_inside_width_limits(707.0)

        assert limits.minimum_mm == 663.5
        assert limits.maximum_mm == 665.0
        assert MOVENTO_760H5000S.drawer_side_length_mm == 490.0
        assert MOVENTO_760H5500S.drawer_side_length_mm == 540.0
        assert MOVENTO_760H5000S.maximum_drawer_side_thickness_mm == 16.0
        assert MOVENTO_760H5000S.drawer_bottom_recess_minimum_mm == 12.0
        assert MOVENTO_760H5000S.drawer_bottom_recess_maximum_mm == 15.0

    def test_inner_front_contributes_to_required_cabinet_depth(self) -> None:
        assert MOVENTO_760H5000S.required_inside_depth_mm() == 503.0
        assert MOVENTO_760H5000S.required_inside_depth_mm(15.0) == 518.0
        assert MOVENTO_760H5500S.required_inside_depth_mm(15.0) == 568.0


class TestMoventoRunnerCatalog:
    """Select runner length without substituting or scaling CAD geometry."""

    def test_first_wardrobe_depth_selects_the_500_runner(self) -> None:
        profile = MOVENTO_RUNNER_CATALOG.select_for_depth(564.0, 15.0)

        assert profile is MOVENTO_760H5000S

    def test_exact_550_depth_requirement_selects_the_longer_runner(self) -> None:
        profile = MOVENTO_RUNNER_CATALOG.select_for_depth(568.0, 15.0)

        assert profile is MOVENTO_760H5500S

    def test_depth_below_every_registered_runner_is_rejected(self) -> None:
        with pytest.raises(MoventoRunnerSelectionError, match="no registered"):
            MOVENTO_RUNNER_CATALOG.select_for_depth(517.0, 15.0)
