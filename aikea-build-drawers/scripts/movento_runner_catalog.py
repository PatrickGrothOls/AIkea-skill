"""Scope: Select the longest registered MOVENTO runner that fits a cabinet."""

from __future__ import annotations

from dataclasses import dataclass

from movento_runner_profile import (
    MoventoHardwareAssetIdentity,
    MoventoHardwareAssetSet,
    MoventoRunnerProfile,
)
from movento_mounting_profile import MOVENTO_760H5000S_MOUNTING


class MoventoRunnerSelectionError(ValueError):
    """Report that no registered runner fits the available cabinet depth."""


MOVENTO_760H5000S = MoventoRunnerProfile(
    product_code="760H5000S",
    item_number="05083446",
    nominal_length_mm=500.0,
    maximum_load_kg=40.0,
    hardware_asset_set=MoventoHardwareAssetSet(
        runner_left=MoventoHardwareAssetIdentity(
            "movento-760h5000s-runner-left",
            "runner-left",
            "760H5000S",
            "05083446",
            "left",
        ),
        runner_right=MoventoHardwareAssetIdentity(
            "movento-760h5000s-runner-right",
            "runner-right",
            "760H5000S",
            "05083446",
            "right",
        ),
        locking_device_left=MoventoHardwareAssetIdentity(
            "t51-7601-left-locking-device",
            "locking-device-left",
            "T51.7601 L",
            "01311197",
            "left",
        ),
        locking_device_right=MoventoHardwareAssetIdentity(
            "t51-7601-right-locking-device",
            "locking-device-right",
            "T51.7601 R",
            "06247277",
            "right",
        ),
    ),
    mounting_profile=MOVENTO_760H5000S_MOUNTING,
    mounting_width_mm=21.0,
    runner_bearing_height_mm=28.5,
    cabinet_profile_width_mm=40.9,
)

MOVENTO_760H5500S = MoventoRunnerProfile(
    product_code="760H5500S",
    item_number="07086828",
    nominal_length_mm=550.0,
    maximum_load_kg=40.0,
    hardware_asset_set=None,
)


@dataclass(frozen=True, slots=True)
class MoventoRunnerCatalog:
    """Own the available runner profiles and their depth-based selection."""

    profiles: tuple[MoventoRunnerProfile, ...]

    def select_for_depth(
        self,
        inside_depth_mm: float,
        inner_front_thickness_mm: float = 0.0,
    ) -> MoventoRunnerProfile:
        candidates = (
            profile
            for profile in self.profiles
            if profile.required_inside_depth_mm(inner_front_thickness_mm)
            <= inside_depth_mm
        )
        try:
            return max(candidates, key=lambda profile: profile.nominal_length_mm)
        except ValueError as error:
            raise MoventoRunnerSelectionError(
                f"no registered MOVENTO runner fits {inside_depth_mm:g} mm"
            ) from error


MOVENTO_RUNNER_CATALOG = MoventoRunnerCatalog(
    profiles=(MOVENTO_760H5000S, MOVENTO_760H5500S),
)


__all__ = [
    "MOVENTO_760H5000S",
    "MOVENTO_760H5500S",
    "MOVENTO_RUNNER_CATALOG",
    "MoventoRunnerCatalog",
    "MoventoRunnerSelectionError",
]
