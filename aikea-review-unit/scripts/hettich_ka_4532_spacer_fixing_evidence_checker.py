"""Scope: Validate saved KA 4532 rail-to-spacer fixing evidence."""

from __future__ import annotations

from math import isfinite
from typing import Any

from hettich_ka_4532_fixed_member_hole_pattern import (
    HETTICH_KA_4532_500_FIXED_MEMBER_HOLES,
)
from hettich_ka_4532_spacer_installed_fixing_checker import (
    HettichKa4532SpacerInstalledFixingChecker,
)
from hettich_ka_4532_spacer_profile import HETTICH_KA_4532_500_WITH_13952


class HettichKa4532SpacerFixingEvidenceChecker:
    """Bind saved machining authority to its exact installed hardware."""

    _MISSING_AUTHORITY = [
        "longer_rail_through_spacer_screw_identity",
        "longer_rail_through_spacer_screw_length_mm",
        "cabinet_pilot_diameter_mm",
        "cabinet_pilot_depth_mm",
    ]

    def __init__(self) -> None:
        self.installed = HettichKa4532SpacerInstalledFixingChecker()

    def matches(
        self,
        machining: dict[str, Any],
        cabinet_id: str,
        drawer_id: str,
        installed_parts: dict[str, Any],
        step_set: Any,
    ) -> bool:
        resolved = machining.get("resolved_authority", {})
        rail = resolved.get("rail_fixed_member_hole_pattern", {})
        spacer = resolved.get("spacer_support_corridor", {})
        pattern = HETTICH_KA_4532_500_FIXED_MEMBER_HOLES
        profile = HETTICH_KA_4532_500_WITH_13952
        return (
            type(machining.get("schema_version")) is int
            and machining.get("schema_version") == 1
            and machining.get("status") == "blocked"
            and machining.get("manufacturing_authority") is False
            and machining.get("cabinet_id") == cabinet_id
            and machining.get("drawer_id") == drawer_id
            and machining.get("spacer_item_number") == profile.spacer_item_number
            and machining.get("reason")
            == "blocked_missing_longer_screw_and_cabinet_pilot"
            and machining.get("missing_authority") == self._MISSING_AUTHORITY
            and rail.get("status") == "verified_against_exact_runner_cad"
            and rail.get("installation_document") == pattern.installation_document
            and rail.get("installation_url") == pattern.installation_url
            and rail.get("hole_diameter_mm") == pattern.hole_diameter_mm
            and rail.get("cabinet_depth_axes_from_front_mm")
            == list(pattern.cabinet_depth_axes_mm)
            and spacer.get("status") == "verified_against_exact_spacer_cad"
            and spacer.get("method")
            == "new_fixing_path_through_solid_spacer_web"
            and spacer.get("preformed_spacer_openings_used") is False
            and spacer.get("width_mm") == profile.spacer_width_per_side_mm
            and spacer.get("asset_id") == profile.spacer_asset_id
            and spacer.get("sha256") == step_set.spacer_source.asset.sha256
            and self._axes_match(
                spacer.get("axes", ()),
                self.installed.axis_height(drawer_id, installed_parts, step_set),
            )
        )

    def _axes_match(
        self,
        axes: list[dict[str, Any]],
        installed_height_mm: float | None,
    ) -> bool:
        if (
            not isinstance(axes, list)
            or len(axes) != 8
            or not all(isinstance(axis, dict) for axis in axes)
            or installed_height_mm is None
        ):
            return False
        heights = tuple(axis.get("cabinet_height_mm") for axis in axes)
        if any(
            type(height_mm) not in (int, float) or not isfinite(height_mm)
            for height_mm in heights
        ):
            return False
        return axes == [
            self._axis(side, index, installed_height_mm)
            for side in ("left", "right")
            for index in range(4)
        ]

    def _axis(self, side: str, index: int, cabinet_height_mm: float) -> dict:
        pattern = HETTICH_KA_4532_500_FIXED_MEMBER_HOLES
        profile = HETTICH_KA_4532_500_WITH_13952
        cabinet_depth_mm = pattern.cabinet_depth_axes_mm[index]
        return {
            "side": side,
            "cabinet_depth_from_front_mm": cabinet_depth_mm,
            "cabinet_height_mm": cabinet_height_mm,
            "runner_native_depth_mm": pattern.fixed_member_native_depth_axes_mm[index],
            "spacer_native_depth_mm": (
                cabinet_depth_mm - profile.spacer_front_from_cabinet_front_mm
            ),
            "spacer_native_height_mm": (
                profile.runner_center_from_drawer_bottom_mm
                - profile.spacer_bottom_from_drawer_bottom_mm
            ),
        }


__all__ = ["HettichKa4532SpacerFixingEvidenceChecker"]
