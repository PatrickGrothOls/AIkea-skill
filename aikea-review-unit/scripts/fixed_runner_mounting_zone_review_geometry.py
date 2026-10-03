"""Scope: Show fixed cabinet-owned runner mounting zones for visual review."""

from __future__ import annotations

from typing import Any

import cadquery as cq

from local_to_parent_location import LocalToParentLocation
from movento_runner_catalog import MOVENTO_760H5000S
from unit_mockup import MockupPart, UnitMockupInputError


class FixedRunnerMountingZoneReviewGeometry:
    """Build non-manufacturing guides from registered runner relationships."""

    _COLOR = (0.23, 0.50, 0.68, 0.45)
    _RUNNER_IDS = ("runner_left", "runner_right")
    _DISPLAY_BAND_HEIGHT_MM = 24.0
    _DISPLAY_BAND_THICKNESS_MM = 12.0

    def __init__(self) -> None:
        self.frame_location = LocalToParentLocation()

    def build(self, built_cabinet: Any) -> tuple[MockupPart, ...]:
        child = self._drawer_child(built_cabinet)
        self._require_registered_fixed_runners(built_cabinet, child)
        profile = MOVENTO_760H5000S
        bearing_height_mm = self._bearing_height(profile)
        box = child.assembly.spec.box
        side_clearance_mm = (
            box.opening.clear_width_mm - box.outside_width_mm
        ) / 2.0
        cabinet_inside_right_mm = box.outside_width_mm + side_clearance_mm
        local_x_positions = (
            -side_clearance_mm,
            cabinet_inside_right_mm - self._DISPLAY_BAND_THICKNESS_MM,
        )
        local_z_mm = -bearing_height_mm - self._DISPLAY_BAND_HEIGHT_MM / 2.0
        frame = self.frame_location.build(child.spec.local_to_parent)
        display_band = cq.Workplane("XY").box(
            self._DISPLAY_BAND_THICKNESS_MM,
            profile.nominal_length_mm,
            self._DISPLAY_BAND_HEIGHT_MM,
            centered=(False, False, False),
        )
        return tuple(
            MockupPart(
                f"review_only__{runner_id}__760h5000s_mounting_zone",
                display_band,
                frame * cq.Location(cq.Vector(local_x_mm, 0.0, local_z_mm)),
                self._COLOR,
            )
            for runner_id, local_x_mm in zip(self._RUNNER_IDS, local_x_positions)
        )

    def _drawer_child(self, built_cabinet: Any) -> Any:
        drawers = tuple(
            child
            for child in built_cabinet.child_assemblies
            if child.spec.purpose == "drawer"
        )
        if len(drawers) != 1:
            raise UnitMockupInputError(
                ["runner mounting-zone review requires exactly one drawer child"]
            )
        return drawers[0]

    def _require_registered_fixed_runners(
        self,
        built_cabinet: Any,
        child: Any,
    ) -> None:
        fixed_runners = tuple(
            hardware
            for hardware in built_cabinet.purchased_hardware
            if hardware.spec.hardware_id in self._RUNNER_IDS
        )
        identities = tuple(hardware.spec.hardware_id for hardware in fixed_runners)
        product_codes = {hardware.spec.product_code for hardware in fixed_runners}
        unresolved_geometry = all(not hardware.has_geometry for hardware in fixed_runners)
        is_supported = (
            identities == self._RUNNER_IDS
            and product_codes == {MOVENTO_760H5000S.product_code}
            and child.assembly.spec.runner_product_code
            == MOVENTO_760H5000S.product_code
            and unresolved_geometry
        )
        if not is_supported:
            raise UnitMockupInputError(
                ["review zones require the unresolved cabinet-owned 500 mm runner pair"]
            )

    def _bearing_height(self, profile: Any) -> float:
        if profile.runner_bearing_height_mm is None:
            raise UnitMockupInputError(
                ["runner profile is missing its registered bearing height"]
            )
        return profile.runner_bearing_height_mm


__all__ = ["FixedRunnerMountingZoneReviewGeometry"]
